'''work in progress'''

import os
from pandas import read_csv, to_datetime
from pathlib import Path


def handle_datetime(df):
    df['date'] = to_datetime(df['date'], format='%a, %d %b %Y %H:%M:%S %z', errors='coerce', utc=True)
            
    # Creating separate columns for Date and Time
    df['Date'] = df['date'].dt.date
    df['Time'] = df['date'].dt.time

    # Handling any remaining NaT values (if any)
    df = df.dropna(subset=['date'])
    
    return df

def kill_duplicates(df):
    df_new = df.drop_duplicates()
    
    try:
        df_new = handle_datetime(df_new)
        
    except:
        pass
    
    return df_new

def main(dataset: list):

    for data in dataset:
        df = read_csv(data)
        # df.info()
        
        df = kill_duplicates(df)
        # gg


