import pandas as pd


def _safe_value(value):
    if pd.isna(value):
        return 0.0
    return float(value)


def generate_insights(df: pd.DataFrame):

    insights = []

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns

    categorical_columns = df.select_dtypes(
        include=["object"]
    ).columns

    # Numerical insights
    for column in numerical_columns:
        series = pd.to_numeric(
            df[column], errors="coerce"
        )
        average = _safe_value(series.mean())
        maximum = _safe_value(series.max())
        minimum = _safe_value(series.min())

        insights.append(
            f"The average {column} is {average:.2f}."
        )

        insights.append(
            f"The maximum {column} is {maximum:.2f}."
        )

        insights.append(
            f"The minimum {column} is {minimum:.2f}."
        )

    # Categorical insights
    for column in categorical_columns:

        if df[column].nunique() > 0:

            most_common = df[column].mode().iloc[0]

            count = int(
                (df[column] == most_common).sum()
            )

            insights.append(
                f"{most_common} is the most frequent "
                f"value in {column}, appearing "
                f"{count} times."
            )

    # Correlation insights
    if len(numerical_columns) >= 2:

        correlation = df[numerical_columns].corr()

        for i in range(len(numerical_columns)):

            for j in range(
                i + 1,
                len(numerical_columns)
            ):

                col1 = numerical_columns[i]
                col2 = numerical_columns[j]

                value = correlation.loc[
                    col1, col2
                ]

                if abs(value) >= 0.7:

                    if value > 0:
                        relationship = (
                            "strong positive"
                        )
                    else:
                        relationship = (
                            "strong negative"
                        )

                    insights.append(
                        f"{col1} and {col2} have a "
                        f"{relationship} correlation "
                        f"of {value:.2f}."
                    )

    return insights