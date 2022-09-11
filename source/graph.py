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
        ax[i].set_ylabel('Timestep')
        if i>0:
            ax[i].axes.get_yaxis().set_visible(False)
        ax[i].axes.get_xaxis().set_visible(False)


    fig.savefig(filename)
    return 0

def visualise_month(frame,hourly_frame,parameter='a1_0',filename='month.pdf'):
    fig,ax=plt.subplots(figsize=(60,5))
    ax.plot(pd.to_datetime(hourly_frame['observe_time'],utc=True),hourly_frame[parameter],marker='D',ls='none',c='red',label='Hourly cadence')

    ax.plot(pd.to_datetime(hourly_frame['observe_time'][hourly_frame[parameter].isna()],utc=True),
            [np.max(hourly_frame[parameter]),]*hourly_frame[parameter][hourly_frame[parameter].isna()].size,marker='D',ls='none',c='green',label='Missing Data')
    ax.annotate(' {:d} missing data'.format(hourly_frame[parameter][hourly_frame[parameter].isna()].size),xy=(0,0.9),xycoords='axes fraction')

    ax.step(pd.to_datetime(frame['observe_time']),frame[parameter],c='k',where='mid',label='Original Data')
    ax.set_xlim(pd.to_datetime(frame['observe_time']).min(),pd.to_datetime(frame['observe_time']).max())
    
    # cosmetics
    from matplotlib.dates import HourLocator, MonthLocator, YearLocator
    ax.xaxis.set_minor_locator(HourLocator(byhour=None, interval=1, tz=None))
    ax.xaxis.set_major_locator(HourLocator(byhour=None, interval=6, tz=None))
    plt.grid()
    plt.xticks(rotation=45,ha='right')
    ax.legend()
    ax.set_xlabel('Time')
    ax.set_ylabel('{}'.format(parameter))
    ax.set_title('Data with 6 hour-grid for {}'.format(parameter))
    fig.tight_layout()
    fig.savefig(filename)
    return 0
