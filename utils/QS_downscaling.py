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
import results
import data_preparation
from PIL import Image
import requests
from io import BytesIO
import os
path = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/Downscaling_CM/G2S"
os.chdir(path)
from g2s import g2s
import time


data_path = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/Downscaling_CM/data"
os.chdir(data_path)

week_2km = xr.open_dataset("week_2km.nc")
week_2km = week_2km.drop('height_2m')
methods = [0, 0, 0]
methods[0] = xr.open_dataset("bilin_week.nc")
methods[1] = xr.open_dataset("bicubic_week.nc")
methods[2] = xr.open_dataset("quintic_week.nc")
ups = xr.open_dataset("week_12km.nc")
methods.append(ups)
names = ["bilinear", "bicubic", "quintic", "coarse resolution"]

ti_fine = data_preparation.QS_ti(1)
ti_T = ti['T_2M'].values
ti_H = ti['RELHUM_2M'].values
ti_PR = ti['TOT_PR'].values


ingrid = rescaling.create_grid(-18.86, 11.98, 0.02, -14.86, 15.98, 0.02)
outgrid = rescaling.create_grid(-18.86, 11.9, 0.12, -14.86, 15.9, 0.12)
ti_coarse = rescaling.upscale(ti, ingrid, outgrid)

tic_T = ti_coarse['T_2M'].values
tic_H = ti_coarse['RELHUM_2M'].values
tic_PR = ti_coarse['TOT_PR'].values

ti = np.stack((ti_T,tic_T),axis=2)

norm =colors.Normalize(vmin=ti_T.min(),vmax=ti_T.max())
f,(ax1,ax2) = plt.subplots(2,1,figsize=(12,12))
ax1.imshow(ti_T,norm=norm)
ax1.set_title('Fine resolution training image')
ax2.imshow(tic_T, norm =norm)
ax2.set_title('Coarse resolution training image')


di_fine = data_preparation.QS_ti(1)
di_T = di['T_2M'].values
di_H = di['RELHUM_2M'].values
di_PR = di['TOT_PR'].values

ingrid = rescaling.create_grid(-18.86, 11.98, 0.02, -14.86, 15.98, 0.02)
outgrid = rescaling.create_grid(-18.86, 11.9, 0.12, -14.86, 15.9, 0.12)
di_coarse = rescaling.upscale(di, ingrid, outgrid)

dic_T = di_coarse['T_2M'].values
dic_H = di_coarse['RELHUM_2M'].values
dic_PR = di_coarse['TOT_PR'].values


fi = dataset.empty_dataset(ti_fine)


di_fine = fi['T_2M'].values
di_coarse = dic_T
di=np.stack((di_fine,di_coarse),axis=2)

#dt consists of two zeros representing two continuous variables
#dt = [0]*ti.shape[-1]

jobid_1=g2s('-a','qs', 
                 '-submitOnly',
                 '-ti',ti,
                 '-di',numpy.zeros((200,200))*numpy.nan,
                 '-dt',[0],
                 '-k',1.2,
                 '-n',50,
                 '-j',0.5);

sim1,_ = g2s('-waitAndDownload',jobid_1)

fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(7,4))
fig.suptitle('QS Unconditional simulation',size='xx-large')
ax1.imshow(di_T)
ax1.set_title('Training image');
ax1.axis('off');
ax2.imshow(sim1)
ax2.set_title('Simulation 1');
ax2.axis('off');
plt.show();
