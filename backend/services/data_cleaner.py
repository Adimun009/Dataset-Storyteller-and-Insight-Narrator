import pandas as pd


def clean_dataset(df: pd.DataFrame):

    cleaning_info = {
        "original_rows": len(df),
        "original_columns": len(df.columns),
        "missing_values_before": int(
            df.isnull().sum().sum()
        ),
        "duplicate_rows_before": int(
            df.duplicated().sum()
        )
    }

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Numerical columns
    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns

    # Fill numerical missing values
    for column in numerical_columns:

        if df[column].isnull().any():

            df[column] = df[column].fillna(
                df[column].median()
            )

    # Categorical columns
    categorical_columns = df.select_dtypes(
        include=["object"]
    ).columns

    # Fill categorical missing values
    for column in categorical_columns:

        if df[column].isnull().any():

            df[column] = df[column].fillna(
                "Unknown"
            )

    cleaning_info["missing_values_after"] = int(
        df.isnull().sum().sum()
    )

    cleaning_info["duplicate_rows_after"] = int(
        df.duplicated().sum()
    )

    cleaning_info["final_rows"] = len(df)

    return df, cleaning_info