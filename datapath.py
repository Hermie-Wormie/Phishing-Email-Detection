import shutil
from pathlib import Path

def extract_data():
    """
    Recreates CLEANDATA folder and child items
    Returns a list of all child items in DATASET
    """
    dataset_dir = Path("DATASET")
    cleandata_dir = Path("CLEANDATA")
    
    ext = "*.csv"
    datasets: list[Path] = []
    datasets.extend(dataset_dir.glob(ext))

    sep_data = read_cleandata(cleandata_dir, ext)

    if cleandata_dir.exists(): shutil.rmtree(cleandata_dir) #in case of corruption
    cleandata_dir.mkdir()
    for path in sep_data:
        path.touch()

    return datasets

def read_cleandata(cleandata_dir=Path("CLEANDATA"), ext="*.csv"):
    """
    Reads CLEANDATA dir
    Returns all child items in CLEANDATA
    """
    datasets: list[Path] = []
    datasets.extend(cleandata_dir.glob(ext))

    return datasets
