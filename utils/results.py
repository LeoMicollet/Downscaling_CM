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

def get_results(ds1, ds_array, methods, step, dim) :
    RMSE = []
    MAE = []
    SSIM = []
    Hellinger = []
    Perkins = []
    
    for ds in ds_array:
       # ds = ds_array[i]
        err = metrics.RMSE(ds1, ds)
        RMSE.append(1 - np.mean(err[dim].values))
        err = metrics.MAE(ds1, ds)
        MAE.append(1 - np.mean(err[dim].values))
        err = metrics.SSIM(ds1, ds)
        SSIM.append(np.mean(err[dim].values))
        err = metrics.Hellinger(ds1, ds, "xarray")
        Hellinger.append(1 - np.mean(err.T_2M.values))
        err = metrics.Perkins(ds1, ds, "xarray")
        Perkins.append(np.mean(err.T_2M.values))
    diff = metrics.compare_corr(ds1, ds_array, methods, len(ds1["time"])//2, step, dim)
    
    
    data = {'method': methods,
            'RMSE': RMSE,
            'MAE': MAE,
            'SSIM': SSIM,
            'Hellinger': Hellinger,
            'Perkins': Perkins,
            'Temporal autocorrelation RMSE': [1-x for x in diff]
    }
    df = pd.DataFrame(data)
    df["mean"] = df.mean(axis=1)
    return df



def joint_pdf(ds, ds_array, dim1, dim2):
    
    binning_data = { 'T_2M': np.linspace(270, 320, 3000),
            'RELHUM_2M': np.linspace(0, 100, 3000),
            'TOT_PR': np.linspace(0, 0.06, 10000)
    }
    
    binning = pd.DataFrame(binning_data)
    
    time_dim = len(ds['time'])
    flat_ds = []
    flat_method = []
    
    flat_ds.append(np.array([ds[dim1].isel(time = k).values.flatten() for k in range(time_dim)]).flatten())
    flat_ds.append(np.array([ds[dim2].isel(time = k).values.flatten() for k in range(len(time_dim))]).flatten())
    pdf, x, y = np.histogram2d(flat_ds[0], flat_ds[1], bins = (binning[dim1], binning[dim2]), density = True)
    
    for method in ds_array:
        flat_method.append(np.array([method[dim1].isel(time = k).values.flatten() for k in range(time_dim)]).flatten())
        flat_method.append(np.array([method[dim2].isel(time = k).values.flatten() for k in range(time_dim)]).flatten())
        pdf_next = np.histogram2d(flat_method[0], flat_method[1], bins = (binning[dim1], binning[dim2]), density = True)
        
        f = lambda y, x: 
        integrate.dblquad(f, binning[dim1][0], binning[dim1][-1], binning[dim2][0], binning[dim2][-1])
        
        
    return 0



