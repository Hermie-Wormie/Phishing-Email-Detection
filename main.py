import os
import shutil
from pathlib import Path
from DATAMANIPULATION.data_clean import main as clean_data

def extract_data():
    dataset_dir = Path("DATASET")
    cleandata_dir = Path("CLEANDATA")
    
    ext = "*.csv"
    datasets: list[Path] = []
    datasets.extend(dataset_dir.glob(ext))

    sep_data: list[Path] = []
    sep_data.extend(cleandata_dir.glob(ext))

    status = cleandata_dir.exists()
    if status:
        # print(f"Removing existing {cleandata_dir} ... ", end="")
        shutil.rmtree(cleandata_dir)
    # print(f"Making {cleandata_dir} ... ", end="")
    cleandata_dir.mkdir()
    for path in sep_data:
        path.touch()

    return datasets

def main():
    
    clean_data(extract_data())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting programme ...")
        exit()