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
        ds = dataset.newdataset(filenames, i*31, i*31+1)[12]
    return ds