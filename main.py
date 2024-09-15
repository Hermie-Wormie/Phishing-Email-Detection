import os
from pathlib import Path
from DATAMANIPULATION.data_clean import *

def extract_data():
    data_path = Path("DATASET")
    
    ext = "*.csv"
    datasets: list[Path] = []
    datasets.extend(data_path.glob(ext))

    # for path in data_path
    return datasets

datainfo(extract_data())