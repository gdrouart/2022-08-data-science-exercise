import numpy as np
import pandas as pd
import glob
import os
import math

def read_folder(foldername):
    """Read the entire month folder and return a dataframe"""
    all_files = glob.glob(os.path.join(foldername , "*.csv"))
    list_file = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header = 0)
        list_file.append(df)

    return pd.concat(list_file, axis=0, ignore_index=True)

def reduce_hourly(frame):
    """
    Take in the full frame and reduce to hourly cadence, 
    replacing parameters values as required (+-10min or NaN)
    """

    tmp_timestamp=pd.to_datetime(frame["observe_time"])
    hourly_frame=frame[tmp_timestamp[tmp_timestamp.dt.minute==0].index]

    # check each row, if nan, check 10min earlier or 10min later and fill frame
    for i,elem in enumerate(hourly_frame):
        if math.isnan(elem):
            current_index = hourly_frame['a1_0'].index[i]
            if ~math.isnan(frame.iloc[current_index-1]['a1_0']):
                hourly_frame.iloc[i,1:]=frame.iloc[current_index-1,1:]
            elif ~math.isnan(frame.iloc[current_index+1]['a1_0']):
                hourly_frame.iloc[i,1:]=frame.iloc[current_index+1,1:]
            else:
                hourly_frame.iloc[i,1:]=np.nan

    # TODO: check graphics it is all good

    return hourly_frame