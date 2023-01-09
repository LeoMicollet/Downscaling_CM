import numpy as np
from matplotlib import pyplot as plt
import math
import xarray as xr
import xskillscore as xs
import skimage
from skimage.metrics import structural_similarity as ssim
import pandas as pd
import seaborn as sns
import dataset

def QS_ti(month):
    """Creates a training dataset for the QS method.

    Parameter:
        month: number of month to take in account.
          
    Return:
        ds: A dataset contaning the first two days of each month at 12 pm.
    """
    filenames = dataset.getfiles()
    for i in month :
        ds = dataset.new_dataset(filenames, i*31, i*31+1)[12]
    return ds

def rescale(ups): 
    """Creates a upscaled dataset from a numpy array with the original images dimensions. Each value is now a square.

    Parameter:
        ups: upscaled dataset.
          
    Return:
        ups_bis: the images are the same as the ups dataset, but with more dimensions.
    """
    ups_bis = np.repeat(ups, 6, axis = 1 )
    ups_bis = np.repeat(ups_bis, 6, axis = 0)
    return ups_bis

def nc_to_np(ds):
    """Converts a netCDF dataset to numpy arrays.

    Parameter:
        ds: .netCDF dataset.
          
    Return:
        array: np.array containing the values from ds.
    """
    array = np.array([ds.T_2M.values, ds.RELHUM_2M.values, ds.TOT_PR.values])
    return array