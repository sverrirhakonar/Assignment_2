from pathlib import Path
import pandas as pd

def build_price_and_volume_frames(folder_path):
    folder = Path(folder_path)
    files = sorted(folder.glob("*.parquet"))
    if not files:
        raise FileNotFoundError("No parquet files found")

    # Base dates from the first file
    first = pd.read_parquet(files[0])
    first.index.name = "Date"
    base_index = first.index

    price_cols = {}
    volume_cols = {}

    for f in files:
        df = pd.read_parquet(f)
        df.index.name = "Date"
        ticker = f.stem
        # collect columns, no per-column assignment into a big frame
        price_cols[ticker] = df["Close"]
        volume_cols[ticker] = df["Volume"]

    # single concat avoids fragmentation
    df_price = pd.concat(price_cols, axis=1).reindex(base_index)
    df_volume = pd.concat(volume_cols, axis=1).reindex(base_index)

    # optional: sort columns
    df_price = df_price.reindex(sorted(df_price.columns), axis=1)
    df_volume = df_volume.reindex(sorted(df_volume.columns), axis=1)

    return df_price, df_volume

# Example usage:
folder_path = r"C:\Users\Lenovo\Documents\FinMath UChicago\Coursework\FINM 32500 1 Computing for Finance in Python\Assignment 2\price_data_by_ticker"
df_price, df_volume = build_price_and_volume_frames(folder_path)

print(df_price.head())
print(df_volume.head())