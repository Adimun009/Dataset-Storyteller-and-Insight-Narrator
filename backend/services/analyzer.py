import pandas as pd


def _safe_float(value):
    if pd.isna(value):
        return 0.0
    return float(value)


def analyze_dataset(df: pd.DataFrame):

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object"]
    ).columns.tolist()

    numerical_summary = {}

    for column in numerical_columns:
        series = pd.to_numeric(
            df[column], errors="coerce"
        )

        numerical_summary[column] = {
            "mean": round(
                _safe_float(series.mean()), 2
            ),
            "median": round(
                _safe_float(series.median()), 2
            ),
            "minimum": round(
                _safe_float(series.min()), 2
            ),
            "maximum": round(
                _safe_float(series.max()), 2
            )
        }

    categorical_summary = {}

    for column in categorical_columns:

        if len(df[column]) > 0:

            categorical_summary[column] = {
                "unique_values": int(
                    df[column].nunique()
                ),
                "most_common": str(
                    df[column].mode().iloc[0]
                )
            }

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "numerical_summary": numerical_summary,
        "categorical_summary": categorical_summary
    }