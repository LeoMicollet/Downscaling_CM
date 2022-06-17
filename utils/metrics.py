import numpy as np
import math
import xarray as xr
import skimage
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error

def SSIM(ds1, ds2) :
    Coordinates = {
        'time':(['time'], ds1.time.values)
    } 
    
    T_2M = []
    TOT_PR = []
    RELHUM_2M = []
    for j in range(len(ds1.time)) :
        T_2M.append(ssim(ds1.T_2M.isel(time = j), ds2.T_2M.isel(time = j)))
        TOT_PR.append(ssim(ds1.TOT_PR.isel(time = j), ds2.TOT_PR.isel(time = j)))
        RELHUM_2M.append(ssim(ds1.RELHUM_2M.isel(time = j), ds2.RELHUM_2M.isel(time = j)))
                
    Variables = {
        'T_2M':(['time'], T_2M),
        'RELHUM_2M':(['time'], RELHUM_2M),
        'TOT_PR':(['time'], TOT_PR)
    }
    SSIM_ds = xr.Dataset(Variables, Coordinates)
    return SSIM_ds

def Hellinger(ds1, ds2) :
    Coordinates = {
        'time':(['time'], ds1.time.values)
    } 

    T_2M = [0]*len(ds1.time)
    TOT_PR = [0]*len(ds1.time)
    RELHUM_2M = [0]*len(ds1.time)
    for k in range(len(ds1.time)) :
        Sum_T = 0
        Sum_PR = 0
        Sum_HUM = 0
        for i in range(len(ds1.rlon)) :
            for j in range(len(ds1.rlat)) :
                Sum_T += (math.sqrt(ds1.T_2M.isel(time = k).values[i][j]) - math.sqrt(ds2.T_2M.isel(time = k).values[i][j]))**2
                Sum_PR += (math.sqrt(ds1.TOT_PR.isel(time = k).values[i][j]) - math.sqrt(ds2.TOT_PR.isel(time = k).values[i][j]))**2
                Sum_HUM += (math.sqrt(ds1.RELHUM_2M.isel(time = k).values[i][j]) - math.sqrt(ds2.RELHUM_2M.isel(time = k).values[i][j]))**2
        T_2M[k] = math.sqrt(Sum_T)*1/math.sqrt(2)
        RELHUM_2M[k] = math.sqrt(Sum_HUM)*1/math.sqrt(2)
        TOT_PR[k] = math.sqrt(Sum_PR)*1/math.sqrt(2)
                
    Variables = {
        'T_2M':(['time'], T_2M),
        'RELHUM_2M':(['time'], RELHUM_2M),
        'TOT_PR':(['time'], TOT_PR)
    }
    H_ds = xr.Dataset(Variables, Coordinates)
    return H_ds