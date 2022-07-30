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
        err = metrics.Hellinger(ds1, ds, "xarray", 0)
        Hellinger.append(1 - np.mean(err.T_2M.values))
        err = metrics.Perkins(ds1, ds, "xarray", 0)
        Perkins.append(np.mean(err.T_2M.values))
        # diff =compare_corr()
    
    
    data = {'method': methods,
            'RMSE': RMSE,
            'MAE': MAE,
            'SSIM': SSIM,
            'Hellinger': Hellinger,
            'Perkins': Perkins,
            'Temporal autocorrelation': diff
    }
    df = pd.DataFrame(data)
    return df

def compare_corr(ds1, ds_array, methods, dim, lag, step): # Helinger is not adaptated
    df = metrics.corr(ds1, dim, lag, step)
    diff = []
    data = []
    data.append(metrics.corr(ds_array[0], dim, lag, step))
    data.append(metrics.corr(ds_array[1], dim, lag, step))
    data.append(metrics.corr(ds_array[2], dim, lag, step))
    
    figure, axis = plt.subplots(len(ds_array)+1)
    
    for i in range(len(ds_array)):
        sns.lineplot(data = df, x="lag", y="corr", ax = axis[i], label = 'real data')
        sns.lineplot(data = data[i], x="lag", y="corr", ax = axis[i], label = methods[i])
        axis[i].set_title("Autocorrelation of normal and " + methods[i])
        
        c = df.copy()
        c['corr'] = np.square(df['corr'] - data[i]['corr'])
        diff.append(c.groupby('lag').mean())
        print(diff[i])
        sns.lineplot(data = diff[i], x="lag", y="corr", ax = axis[len(ds_array)], label = methods[i] + ' MSE')
    
    axis[len(ds_array)].set_title("MSE")
    RMSE = [np.mean(val['corr'].values)**1/2 for val in diff]
    return RMSE

def joint_pdf(ds, ds_array, dim1, dim2):
    time_dim = len(ds['time'])
    flat_ds = []
    flat_method = []
    
    flat_ds.append(np.array([ds[dim1].isel(time = k).values.flatten() for k in range(time_dim)]).flatten())
    flat_ds.append(np.array([ds[dim2].isel(time = k).values.flatten() for k in range(len(time_dim))]).flatten())
    
    for method in ds_array:
        flat_method.append(np.array([method[dim1].isel(time = k).values.flatten() for k in range(time_dim)]).flatten())
        flat_method.append(np.array([method[dim2].isel(time = k).values.flatten() for k in range(time_dim)]).flatten())
        
        
        
    return 0



