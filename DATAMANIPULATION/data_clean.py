'''work in progress'''

import os
from pandas import read_csv
from pathlib import Path


def datainfo(dataset: list):

    for data in dataset:
        df = read_csv(data)
        df.info()

