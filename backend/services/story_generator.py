import pandas as pd


def _safe_value(value):
    if pd.isna(value):
        return 0.0
    return float(value)


def generate_story(df: pd.DataFrame):

    rows = len(df)
    columns = len(df.columns)

    story = (
        f"The dataset contains {rows} records "
        f"and {columns} columns. "
    )

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns

    if len(numerical_columns) > 0:

        story += (
            "The numerical analysis reveals "
            "several important patterns. "
        )

        for column in numerical_columns[:3]:
            series = pd.to_numeric(
                df[column], errors="coerce"
            )
            average = _safe_value(series.mean())

            story += (
                f"The average {column} is "
                f"{average:.2f}. "
            )

    categorical_columns = df.select_dtypes(
        include=["object"]
    ).columns

    if len(categorical_columns) > 0:

        column = categorical_columns[0]

        most_common = df[column].mode().iloc[0]

        story += (
            f"The most frequently occurring "
            f"{column} is {most_common}. "
        )

    story += (
        "Overall, the system transforms raw data "
        "into meaningful information and insights."
    )

    return story