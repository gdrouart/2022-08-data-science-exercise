import numpy as np
import pandas as pd
import glob
import os
import math

from source.graph import visualise_parameters
from source.graph import visualise_month

def read_folder(foldername):
    """Read the entire month folder and return a dataframe"""
    all_files = glob.glob(os.path.join(foldername , "*.csv"))
    all_files.sort()

    check_len=np.vectorize(len)

    list_file = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header = 0, on_bad_lines='skip')
        try:
            size_date=check_len(df['observe_time'])
        except:
            print(filename)
        df=df[size_date>24]
        list_file.append(df)

    frame = pd.concat(list_file, axis=0, ignore_index=True)

    # making sure that the frame is only float - excepted first column (Cheeky Kevin)
    # TODO: check with pipeline if all parameters are required to be finite
    frame.iloc[:,1:]=frame.iloc[:,1:].apply(pd.to_numeric,errors='coerce')
    return frame

def reduce_hourly(frame):
    """
    Take in the full frame and reduce to hourly cadence, 
    replacing parameters values as required (+-10min or NaN)
    """

    tmp_timestamp=pd.to_datetime(frame["observe_time"],utc=True)

    # create the hourly cadence dataframe
    hourly_frame=pd.DataFrame(columns=frame.columns)


    # create the 1h scaling from existing dataframe
    scale=pd.date_range('{}-{}'.format(*[tmp_timestamp[0].year,tmp_timestamp[0].month]),
                        '{}-{}'.format(*[tmp_timestamp[0].year,tmp_timestamp[0].month+1]),
                        freq='h',inclusive='left',tz='UTC')

    for i,elem in enumerate(scale):
        tmp=np.where(elem==tmp_timestamp)[0]
        if tmp.size > 0:
            hourly_frame=pd.concat([hourly_frame,frame.iloc[tmp]])
        else:
            if np.where(elem-pd.Timedelta('10min')==tmp_timestamp)[0].size > 0:
                tmp=np.where(elem-pd.Timedelta('10min')==tmp_timestamp)[0]
                hourly_frame=pd.concat([hourly_frame,frame.iloc[tmp]])
                hourly_frame.loc[hourly_frame.index[-1],('observe_time')]=elem
            elif np.where(elem+pd.Timedelta('10min')==tmp_timestamp)[0].size > 0:
                tmp=np.where(elem+pd.Timedelta('10min')==tmp_timestamp)[0]
                hourly_frame=pd.concat([hourly_frame,frame.iloc[tmp]])
                hourly_frame.loc[hourly_frame.index[-1],('observe_time')]=elem
            else:                
                hourly_frame=pd.concat([hourly_frame,pd.Series([np.nan])])
                hourly_frame.iat[-1,0]=elem

    # produce graphics it is all good
    timestamp_str=[tmp_timestamp.dt.year[0],tmp_timestamp.dt.month[0]]
    visualise_parameters(frame,filename='full_frame_{:d}-{:d}_parameters.pdf'.format(*timestamp_str))
    visualise_parameters(hourly_frame,filename='hourly_frame_{:d}-{:d}_parameters.pdf'.format(*timestamp_str))
    print('Files for full frame and hourly candence. Check for white stripes for NaN!')
    visualise_month(frame,hourly_frame,filename='{:d}-{:d}_data.pdf'.format(*timestamp_str),parameter='a1_0')

    # code check for missing values:
    print('There are {} Nan values in the hourly cadence file.'.format(hourly_frame[hourly_frame['a1_0'].isna()].size))
    print('This represents {} lines'.format(hourly_frame[hourly_frame['a1_0'].isna()].size/701))
    print('No panic, this might be normal, but you might want to double check!')

    print("")
    print("Writing the hourly cadence into a file")
    # TODO: check with ML pipeline to optimise format choice. Meanwhile, save as csv
    hourly_frame.to_csv('{}_{}_hourly.csv'.format(*timestamp_str),header=True,index=False)
    return hourly_frame

def main():
    data = read_folder("../data/2022-08/")
    data_hourly = reduce_hourly(data)
    print('test done for August 2022')

if __name__ == "__main__":
    main()
