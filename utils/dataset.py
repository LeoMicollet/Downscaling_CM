import xarray as xr
import numpy as np
import os
import glob
from matplotlib import pyplot as plt

def getfiles() : # Create a list with all the file names
    filenames  = glob.glob("lffd*")
    filenames = sorted(filenames)
    return filenames

def summer_ds(fnames) : # Create a new dataset containing all the values during the summer
    summer = [xr.open_dataset(file) for file in fnames[172*24:265*24]]
    sorted_summer = [xr.merge([file.T_2M, file.RELHUM_2M, file.TOT_PR]) for file in summer]
    summer_dataset = xr.concat(sorted_summer, dim='time')
    return summer_dataset

#winter_ds not working
def winter_ds(fnames) : # Create a new dataset containing all the values during the winter
    winter = [xr.open_dataset(file) for file in [fnames[:80*24] + fnames[356*24:]]]
    sorted_winter = [xr.merge([file.T_2M, file.RELHUM_2M, file.TOT_PR]) for file in winter]
    winter_dataset = xr.concat(sorted_winter, dim='time')
    return winter_dataset

def new_dataset(fnames, first_day, last_day) : # Create a new dataset containing all the values between first and last day
    fd = first_day*24
    ld = last_day*24
    dataset = [xr.open_dataset(file) for file in fnames[fd:ld]]
    sorted_ds = [xr.merge([file.T_2M, file.RELHUM_2M, file.TOT_PR]) for file in dataset]
    dataset = xr.concat(sorted_ds, dim='time')
    return dataset

def empty_dataset(ds) : # Creates a dataset full of 0, the same shape as ds
    empty_ds = xr.full_like(ds, 0)
    return empty_ds

def save_dataset(ds, name) : # Saves the dataset
    filename = './'+name+'.nc'
    print ('saving to ', filename)
    ds.to_netcdf(path=filename)
    ds.close()
    print ('finished saving')