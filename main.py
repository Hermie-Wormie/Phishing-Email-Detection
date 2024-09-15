import os
from pathlib import Path
from DATAMANIPULATION.data_clean import main as clean_data

def extract_data():
    data_path = Path("DATASET")
    
    ext = "*.csv"
    datasets: list[Path] = []
    datasets.extend(data_path.glob(ext))

    # for path in data_path
    return datasets

def main():
    
    clean_data(extract_data())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting programme ...")
        exit()