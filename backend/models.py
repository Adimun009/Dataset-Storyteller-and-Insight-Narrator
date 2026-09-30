from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())

    rows = Column(Integer)
    columns = Column(Integer)

    missing_values = Column(Integer)
    duplicate_rows = Column(Integer)

    insights = relationship(
        "Insight",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )
    stories = relationship(
        "Story",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )


class Insight(Base):
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)

    dataset_id = Column(
        Integer,
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False
    )

    insight_text = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    dataset = relationship("Dataset", back_populates="insights")


Index("ix_insights_dataset_id", Insight.dataset_id)


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)

    dataset_id = Column(
        Integer,
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False
    )

    story_text = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    dataset = relationship("Dataset", back_populates="stories")


Index("ix_stories_dataset_id", Story.dataset_id)