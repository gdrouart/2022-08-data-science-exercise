import numpy as np
import pandas as pd
import glob
import os
import math

from graph import visualise_parameters

def read_folder(foldername):
    """Read the entire month folder and return a dataframe"""
    all_files = glob.glob(os.path.join(foldername , "*.csv"))
    all_files.sort()

    list_file = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header = 0)
        list_file.append(df)

    frame = pd.concat(list_file, axis=0, ignore_index=True)
    return frame

def reduce_hourly(frame):
    """
    Take in the full frame and reduce to hourly cadence, 
    replacing parameters values as required (+-10min or NaN)
    """

    tmp_timestamp=pd.to_datetime(frame["observe_time"])
    hourly_frame=frame.iloc[tmp_timestamp[tmp_timestamp.dt.minute==0].index]
    hourly_frame = hourly_frame.iloc[:-1]

    # check each row, if nan, check 10min earlier or 10min later and fill frame
    for i,elem in enumerate(hourly_frame['a1_0']):
        if math.isnan(elem):
            current_index = hourly_frame['a1_0'].index[i]
            if ~math.isnan(frame.iloc[current_index-1]['a1_0']):
                hourly_frame.iloc[i,1:]=frame.iloc[current_index-1,1:]
            elif ~math.isnan(frame.iloc[current_index+1]['a1_0']):
                hourly_frame.iloc[i,1:]=frame.iloc[current_index+1,1:]
            else:
                hourly_frame.iloc[i,1:]=np.nan

    # check graphics it is all good
    timestamp_str= [tmp_timestamp.dt.year[0],tmp_timestamp.dt.month[0]]
    visualise_parameters(frame,filename='full_frame_{}-{}_parameters.pdf'.format(*timestamp_str))
    visualise_parameters(hourly_frame,filename='hourly_frame_{}-{}_parameters.pdf'.format(*timestamp_str))
    print('Files for full frame and hourly candence. Check for white stripes for NaN!')

    # code check for missing values:
    print('There are {} Nan values in the hourly cadence file'.format(hourly_frame[hourly_frame['a1_0'].isna()].size))
    print('No panic, this might be normal, but you might want to double check!')

    return hourly_frame

def main():
    data = read_folder("../data/2022-06/")
    data_hourly = reduce_hourly(data)
    print('done for June 2022')


if __name__ == "__main__":
    main()
