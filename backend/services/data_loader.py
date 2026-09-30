import pandas as pd


def load_dataset(file_path: str) -> pd.DataFrame:

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)

    elif file_path.endswith(".xls"):
        df = pd.read_excel(file_path)

    else:
        raise ValueError(
            "Unsupported file format. Use CSV or Excel."
        )

    return df