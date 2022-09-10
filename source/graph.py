import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def visualise_parameters(frame,filename='param.pdf'):
    """Take a frame and plot a 2D projection of paramters"""

    # isolate the parameters ranges:
    a1=np.arange(1,101)
    a2=np.arange(1,101)+100
    b1=np.arange(1,101)+200
    b2=np.arange(1,101)+300
    hspec=np.arange(1,101)+400
    dspec=np.arange(1,101)+500
    sprspec=np.arange(1,101)+600
    param=['a1','a2','b1','b2','hspec','dspec','sprspec']

    fig,ax=plt.subplots(1,7,figsize=(6,20))
    for i,elem in enumerate([a1,a2,b1,b2,hspec,dspec,sprspec]):
        ax[i].imshow(frame.iloc[:,elem],aspect=1)
        ax[i].set_title(param[i])

    fig.savefig(filename)
    return 0
