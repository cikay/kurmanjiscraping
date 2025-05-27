import pandas as pd


def count_rows_with_pandas(file_path):
    df = pd.read_csv(file_path)
    return len(df)


# Example usage
file_path = "mezopotamya.csv"
count = count_rows_with_pandas(file_path)
print(f"The CSV file contains {count} rows (excluding header).")
