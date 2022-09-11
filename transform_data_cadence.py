import source.utilities as ut
import source.graph as gp
# import numpy as np
# import pandas as pd

folders_to_tranform=['data/2022-06','data/2022-07','data/2022-08']

for i in folders_to_tranform:
    data = ut.read_folder(i)
    data_hourly = ut.reduce_hourly(data)
    print('Done for {}'.format(i))
