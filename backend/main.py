import os

from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine
from services.analyzer import analyze_dataset
from services.data_cleaner import clean_dataset
from services.data_loader import load_dataset
from services.insight_engine import generate_insights
from services.story_generator import generate_story


# -------------------------------------------------
# CREATE FASTAPI APPLICATION
# -------------------------------------------------

app = FastAPI(
    title="Dataset Storyteller API",
    description=(
        "AI-powered dataset analysis "
        "and insight generation API"
    ),
    version="1.0.0"
)


# -------------------------------------------------
# CORS
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# UPLOAD FOLDER
# -------------------------------------------------

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# -------------------------------------------------
# DATABASE
# -------------------------------------------------


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def serialize_dataset(dataset, include_results=False):
    result = {
        "id": dataset.id,
        "filename": dataset.filename,
        "upload_date": dataset.upload_date.isoformat() if dataset.upload_date else None,
        "rows": dataset.rows,
        "columns": dataset.columns,
        "missing_values": dataset.missing_values,
        "duplicate_rows": dataset.duplicate_rows,
    }
    if include_results:
        result["insights"] = [
            {
                "id": insight.id,
                "insight_text": insight.insight_text,
                "created_at": insight.created_at.isoformat() if insight.created_at else None,
            }
            for insight in dataset.insights
        ]
        result["stories"] = [
            {
                "id": story.id,
                "story_text": story.story_text,
                "created_at": story.created_at.isoformat() if story.created_at else None,
            }
            for story in dataset.stories
        ]
    return result


# -------------------------------------------------
# HOME ROUTE
# -------------------------------------------------

@app.get("/")
def home():

    return {
        "message": (
            "Dataset Storyteller Backend "
            "is running!"
        )
    }


@app.get("/datasets")
def list_datasets(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    datasets = (
        db.query(models.Dataset)
        .order_by(models.Dataset.upload_date.desc(), models.Dataset.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [serialize_dataset(dataset) for dataset in datasets]


@app.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return serialize_dataset(dataset, include_results=True)


@app.delete("/datasets/{dataset_id}")
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    db.delete(dataset)
    db.commit()
    return {"message": "Dataset deleted", "dataset_id": dataset_id}


# -------------------------------------------------
# ANALYZE DATASET
# -------------------------------------------------

@app.post("/analyze")
async def analyze_dataset_api(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Check file
    if not file.filename:
        return {
            "error": "No file selected"
        }

    # Create file path
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    # Save uploaded file
    contents = await file.read()

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(contents)

    # Load dataset
    df = load_dataset(file_path)

    # Clean dataset
    cleaned_df, cleaning_info = (
        clean_dataset(df)
    )

    # Analyze dataset
    analysis = analyze_dataset(
        cleaned_df
    )

    # Generate insights
    insights = generate_insights(
        cleaned_df
    )

    # Generate story
    story = generate_story(
        cleaned_df
    )

    # Dataset preview
    preview = (
        cleaned_df
        .head(10)
        .fillna("")
        .to_dict(orient="records")
    )

    # Save dataset metadata in database
    dataset_record = models.Dataset(
        filename=file.filename,
        rows=analysis["rows"],
        columns=analysis["columns"],
        missing_values=cleaning_info["missing_values_after"],
        duplicate_rows=cleaning_info["duplicate_rows_after"],
    )
    try:
        db.add(dataset_record)
        db.flush()

        dataset_record.insights = [
            models.Insight(insight_text=insight)
            for insight in insights
        ]
        dataset_record.stories = [models.Story(story_text=story)]
        db.commit()
        db.refresh(dataset_record)
    except Exception:
        db.rollback()
        raise

    # Return results
    return {
        "dataset_id": dataset_record.id,
        "filename": file.filename,
        "cleaning": cleaning_info,
        "analysis": analysis,
        "insights": insights,
        "story": story,
        "preview": preview
    }