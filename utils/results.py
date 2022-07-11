import numpy as np
from matplotlib import pyplot as plt
import math
import xarray as xr
import xskillscore as xs
import skimage
from skimage.metrics import structural_similarity as ssim
import pandas as pd
import seaborn as sns
import metrics

def get_results(ds1, ds_array, methods) :
    RMSE = []
    MAE = []
    SSIM = []
    Hellinger = []
    Perkins = []
    
    for ds in ds_array:
       # ds = ds_array[i]
        err = metrics.RMSE(ds1, ds)
        RMSE.append(1 - np.mean(err.T_2M.values))
        err = metrics.MAE(ds1, ds)
        MAE.append(1 - np.mean(err.T_2M.values))
        err = metrics.SSIM(ds1, ds)
        SSIM.append(np.mean(err.T_2M.values))
        err = metrics.Hellinger(ds1,ds)
        Hellinger.append(np.mean(err.T_2M.values))
        err = metrics.Perkins(ds1,ds)
        Perkins.append(1 - np.mean(err.T_2M.values))
        
    
    
    data = {'method': methods,
            'RMSE': RMSE,
            'MAE': MAE,
            'SSIM': SSIM,
            'Hellinger': Hellinger,
            'Perkins': Perkins
    }
    df = pd.DataFrame(data)
    return df

def compare_corr(ds1, ds_array, methods, dim, lag, step):
    df = metrics.corr(ds1, dim, lag, step)
    data = []
    data.append(metrics.corr(ds_array[0], dim, lag, step))
    data.append(metrics.corr(ds_array[1], dim, lag, step))
    data.append(metrics.corr(ds_array[2], dim, lag, step))
    
    figure, axis 0plt.sunplot(len(ds_array),2)
    
    for i in range(len(ds_array)):
        sns.lineplot(data = df, x="lag", y="corr", ax = axis[i,0])
        sns.lineplot(data = data[i], x="lag", y="corr", ax = axis[i,0])
        axis[i,0].set_title("Autocorrelation of normal and " method[i])
        sns.lineplot(data = df, x="lag", y="corr", ax = axis[i,1])
        sns.lineplot(data = abs(df - data[i])*100, x="lag", y="corr", ax = axis[i,1])
        axis[i,0].set_title("Difference" method[i])        
        
    return 0