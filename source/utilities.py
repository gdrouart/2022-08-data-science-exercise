import numpy as np
import pandas as pd
import glob
import os


def read_folder(foldername):
    """Read the entire month folder and return a dataframe"""
    all_files = glob.glob(os.path.join(foldername , "*.csv"))
    list_file = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header = 0)
        list_file.append(df)

    return pd.concat(list_file, axis=0, ignore_index=True)

