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
    filenames = dataset.getfiles()
    for i in month :
        ds = dataset.new_dataset(filenames, i*31, i*31+1)[12]
    return ds

def rescale(ups): #works with an numpy array
    ups_bis = np.repeat(ups, 6, axis = 1 )
    ups_bis = np.repeat(ups_bis, 6, axis = 0)
    return ups_bis

def nc_to_np(ds):
    array = np.array([ds.T_2M.values, ds.RELHUM_2M.values, ds.TOT_PR.values])
    return array