import pandas as pd

def convert_df_to_csv(df):
    """
    Converts a Pandas DataFrame to a CSV string for download.
    """
    return df.to_csv(index=False).encode('utf-8')