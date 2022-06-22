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

def discrete_Hellinger(ds1, ds2) :
    Coordinates = {
        'time':(['time'], ds1.time.values)
    } 

    T_2M = []
    TOT_PR = []
    RELHUM_2M = []
    for k in range(len(ds1.time)) :
        Array_T = np.square(np.sqrt(ds1.T_2M.isel(time = k).values) - np.sqrt(ds2.T_2M.isel(time = k).values))
        Array_PR = np.square(np.sqrt(ds1.TOT_PR.isel(time = k).values) - np.sqrt(ds2.TOT_PR.isel(time = k).values))
        Array_HUM = np.square(np.sqrt(ds1.RELHUM_2M.isel(time = k).values) - np.sqrt(ds2.RELHUM_2M.isel(time = k).values))
        T_2M.append(math.sqrt(np.sum(Array_T))*1/math.sqrt(2))
        RELHUM_2M.append(math.sqrt(np.sum(Array_HUM))*1/math.sqrt(2))
        TOT_PR.append(math.sqrt(np.sum(Array_PR))*1/math.sqrt(2))
    Variables = {
        'T_2M':(['time'], T_2M),
        'RELHUM_2M':(['time'], RELHUM_2M),
        'TOT_PR':(['time'], TOT_PR)
    }
    H_ds = xr.Dataset(Variables, Coordinates)
    return H_ds

def Hellinger(ds1,ds2) :
    Coordinates = {
        'time':(['time'], ds1.time.values)
    } 
    T_2M = []
    TOT_PR = []
    RELHUM_2M = []
    bins_T = np.linspace(270,320,3000)
    bins_HUM = np.linspace(0,100,3000)
    bins_PR = np.linspace(0,0.06,10000)
    
    for k in range(len(ds1.time)) :
        pdf1, bin_out = np.histogram(ds1.T_2M.isel(time = k).values, bins_T, density = True) 
        pdf2, bin_out = np.histogram(ds2.T_2M.isel(time = k).values, bins_T, density = True)
        int_T = 1 - np.trapz(np.sqrt(np.multiply(pdf1, pdf2)),bins_T[1:])
        
        pdf1, bin_out = np.histogram(ds1.TOT_PR.isel(time = k).values, bins_PR, density = True) 
        pdf2, bin_out = np.histogram(ds2.TOT_PR.isel(time = k).values, bins_PR, density = True)
        int_PR = 1 - np.trapz(np.sqrt(np.multiply(pdf1, pdf2)),bins_PR[1:])
        
        pdf1, bin_out = np.histogram(ds1.RELHUM_2M.isel(time = k).values, bins_HUM, density = True) 
        pdf2, bin_out = np.histogram(ds2.RELHUM_2M.isel(time = k).values, bins_HUM, density = True)
        int_HUM = 1 - np.trapz(np.sqrt(np.multiply(pdf1, pdf2)),bins_HUM[1:])
        
        T_2M.append(math.sqrt(int_T))
        RELHUM_2M.append(math.sqrt(int_HUM))
        TOT_PR.append(math.sqrt(int_PR))
        
    Variables = {
        'T_2M':(['time'], T_2M),
        'RELHUM_2M':(['time'], RELHUM_2M),
        'TOT_PR':(['time'], TOT_PR)
    }
    H_ds = xr.Dataset(Variables, Coordinates)
    return H_ds

def Perkins(ds1, ds2) :
    Coordinates = {
        'time':(['time'], ds1.time.values)
    } 
        
    T_2M = []
    TOT_PR = []
    RELHUM_2M = []
    bins_T = np.linspace(270,320,3000)
    bins_HUM = np.linspace(0,100,3000)
    bins_PR = np.linspace(0,0.06,10000)
    
    for k in range(len(ds1.time)) :
        pdf1, bin_out = np.histogram(ds1.T_2M.isel(time = k).values, bins_T, density = True) 
        pdf2, bin_out = np.histogram(ds2.T_2M.isel(time = k).values, bins_T, density = True)
        T_2M.append(np.trapz(np.minimum(pdf1, pdf2), bins_T[1:]))
        
        pdf1, bin_out = np.histogram(ds1.TOT_PR.isel(time = k).values, bins_PR, density = True) 
        pdf2, bin_out = np.histogram(ds2.TOT_PR.isel(time = k).values, bins_PR, density = True)
        TOT_PR.append(np.trapz(np.minimum(pdf1, pdf2), bins_PR[1:]))

        pdf1, bin_out = np.histogram(ds1.RELHUM_2M.isel(time = k).values, bins_HUM, density = True) 
        pdf2, bin_out = np.histogram(ds2.RELHUM_2M.isel(time = k).values, bins_HUM, density = True)
        RELHUM_2M.append(np.trapz(np.minimum(pdf1, pdf2), bins_HUM[1:]))
        
    Variables = {
        'T_2M':(['time'], T_2M),
        'RELHUM_2M':(['time'], RELHUM_2M),
        'TOT_PR':(['time'], TOT_PR)
    }
    P_ds = xr.Dataset(Variables, Coordinates)
    return P_ds