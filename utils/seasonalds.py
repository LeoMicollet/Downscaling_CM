import numpy as np
import xarray as xr
import os
import glob
from matplotlib import pyplot as plt
%matplotlib inline


filenames  = glob.glob("lffd*")
filenames = sorted(filenames)

def summer_ds(filenames) :
    summer = [xr.open_dataset(file) for file in filenames[172*24:265*24]]
    sorted_summer = [xr.merge([file.T_2M, file.RELHUM_2M, file.TOT_PR]) for file in summer];
    summer_dataset = xr.concat(sorted_summer, dim='time')
    return summer_dataset

def winter_ds(filenames) :
    winter = [xr.open_dataset(file) for file in [filenames[:80*24] + filenames[356*24:]]]
    sorted_winter = [xr.merge([file.T_2M, file.RELHUM_2M, file.TOT_PR]) for file in winter];sorted_winter
    winter_dataset = xr.concat(sorted_winter, dim='time')
    return winter_dataset
