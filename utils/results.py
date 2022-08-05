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

def get_results(ds1, ds_array, methods, dim, pixel_len) :
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
    diff = metrics.compare_corr(ds1, ds_array, methods, len(ds1["time"])//2, dim)
    
    
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
    
    binning = { 'T_2M': np.linspace(27000, 32000, 501)/100,
            'RELHUM_2M': np.linspace(0,100000,1001)/1000,
            'TOT_PR': np.linspace(0, 6000000, 60001)/1000000
    }
    
    round_val = { 'T_2M': 1,
            'RELHUM_2M': 1,
            'TOT_PR': 6
    }
    
    options={'limit':100}
    
    time_dim = len(ds['time'])
    flat_ds = []
    flat_method = []
    
    H = []
    P = []
    
    flat_ds.append(np.array([ds[dim1].isel(time = k).values.flatten() for k in range(time_dim)]).flatten())
    flat_ds.append(np.array([ds[dim2].isel(time = k).values.flatten() for k in range(time_dim)]).flatten())
    pdf, bin1, bin2 = np.histogram2d(flat_ds[0], flat_ds[1], bins = (binning[dim1], binning[dim2]), density = True)
    
    for method in ds_array:
        flat_method.append(np.array([method[dim1].isel(time = k).values.flatten() for k in range(time_dim)]).flatten())
        flat_method.append(np.array([method[dim2].isel(time = k).values.flatten() for k in range(time_dim)]).flatten())
        pdf_next, bin1_next, bin2_next = np.histogram2d(flat_method[0], flat_method[1], bins = (binning[dim1], binning[dim2]), density = True)
        
        
        def f_H(x, y):
            x = round(x, round_val[dim1])
            y = round(y,round_val[dim2])
            i = list(binning[dim1][:-1]).index(x)
            j = list(binning[dim2][:-1]).index(y)
            f = ((pdf[i, j])**1/2 - (pdf_next[i, j])**1/2)**2
            return f
            
       # H_int, err = integrate.dblquad(f_H, binning[dim1][0], binning[dim1][-2], binning[dim2][0], binning[dim2][-2]) The issue with dblquad is thqt the number of iterqation cannot be modifiewd
        H_int, err  = integrate.nquad(f_H, [[binning[dim1][0], binning[dim1][-2]],[binning[dim2][0], binning[dim2][-2]]], opts = [options, options])
        print(H_int)
        H.append(math.sqrt(H_int))
        
        
        def f_P(x, y):
            x = round(x, round_val[dim1])
            y = round(y,round_val[dim2])
            i = list(binning[dim1][:-1]).index(x)
            j = list(binning[dim2][:-1]).index(y)            
            f = np.minimum(pdf[i, j],pdf_next[i, j])
            return f
        
        P_int, err = integrate.nquad(f_P, [[binning[dim1][0], binning[dim1][-2]],[binning[dim2][0], binning[dim2][-2]]], opts = [options, options])
        P.append(P_int)
        
    data = {'method': methods,
            'Hellinger': H,
            'Perkins': P
    }
    df = pd.DataFrame(data)
    df["mean"] = df.mean(axis=1)
    return df



