import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt
import math
import xarray as xr
import xskillscore as xs
import skimage
from skimage.metrics import structural_similarity as ssim
import pandas as pd
import seaborn as sns
import metrics

def get_results(ds1, upscaled, ds_array, methods, dim, pixel_len) :
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
        Hellinger.append(1 - np.mean(err[dim].values))
        err = metrics.Perkins(ds1, ds, "xarray")
        Perkins.append(np.mean(err[dim].values))
    diff = metrics.compare_corr(ds1, ds_array, methods, 'time', len(ds1["time"])//2, dim, pixel_len)
    ds_array.append(upscaled)
    methods.append('upscaling')
    diffx = metrics.compare_corr(ds1, ds_array, methods, 'rlon', len(ds1["time"])//2, dim, pixel_len)
    diffy = metrics.compare_corr(ds1, ds_array, methods, 'rlat', len(ds1["time"])//2, dim, pixel_len)

    
    data = {'method': methods[:-1],
            'RMSE': RMSE,
            'MAE': MAE,
            'SSIM': SSIM,
            'Hellinger': Hellinger,
            'Perkins': Perkins,
            'Temporal autocorrelation RMSE': [1-x for x in diff],
            'Spatial autocorrelation RMSE (longitude)': [1-x for x in diffx],
            'Spatial autocorrelation RMSE (latitude)': [1-x for x in diffy]
    }
    df = pd.DataFrame(data)
    df["mean"] = df.mean(axis=1)
    return df







