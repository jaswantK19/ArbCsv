import pandas as pd

def get_schema(file_path: str):
    df = pd.read_csv(file_path)
    return df

