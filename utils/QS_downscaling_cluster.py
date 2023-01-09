import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt
from matplotlib import colors
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
from g2s import g2s
import time
import rescaling
import dataset

data_path = "/Users/leomi/Documents/PRe/Downscaling_CM/data"
os.chdir(data_path)

week_2km = xr.open_dataset("week_2km.nc")
week_2km = week_2km.drop('height_2m')
ups = xr.open_dataset("week_12km.nc")
month = [1]
#ti_fine = data_preparation.QS_ti(month)
ti_fine = week_2km.isel(time = 1)
ti_T = ti_fine['T_2M'].values
ti_H = ti_fine['RELHUM_2M'].values
ti_PR = ti_fine['TOT_PR'].values


#ingrid = rescaling.create_grid(-18.86, 11.98, 0.02, -14.86, 15.98, 0.02)
#outgrid = rescaling.create_grid(-18.86, 11.9, 0.12, -14.86, 15.9, 0.12)

#ti_coarse = rescaling.upscale(ti, ingrid, outgrid)
ti_coarse = ups.isel(time = 8)
tic_T = data_preparation.rescale(ti_coarse['T_2M'].values)
tic_H = ti_coarse['RELHUM_2M'].values
tic_PR = ti_coarse['TOT_PR'].values



ti = np.stack((ti_T[:500,:500],tic_T[:500,:500]),axis=2)

norm =colors.Normalize(vmin=ti_T.min(),vmax=ti_T.max())
f,(ax1,ax2) = plt.subplots(2,1,figsize=(12,12))
ax1.imshow(ti_T[:500,:500])
ax1.set_title('Fine resolution training image')
ax2.imshow(tic_T[:500,:500], norm =norm)
#ax2.imshow(tic_T[:500,:500])
ax2.set_title('Coarse resolution training image')


#di_fine = data_preparation.QS_ti(month)
#di_T = di['T_2M'].values
#di_H = di['RELHUM_2M'].values
#di_PR = di['TOT_PR'].values

#ingrid = rescaling.create_grid(-18.86, 11.98, 0.02, -14.86, 15.98, 0.02)
#outgrid = rescaling.create_grid(-18.86, 11.9, 0.12, -14.86, 15.9, 0.12)
#di_coarse = rescaling.upscale(di, ingrid, outgrid)
di_coarse = ups.isel(time = 14)

dic_T = data_preparation.rescale(di_coarse['T_2M'].values)
dic_H = di_coarse['RELHUM_2M'].values
dic_PR = di_coarse['TOT_PR'].values


fi = dataset.empty_dataset(ti_fine,0)


di_fine = np.empty((1542,1542,))*np.nan
di_coarse = dic_T
di=np.stack((di_fine[:500,:500],di_coarse[:500,:500]),axis=2)

norm =colors.Normalize(vmin=ti_T.min(),vmax=ti_T.max())
f,(ax1,ax2) = plt.subplots(2,1,figsize=(12,12))
ax1.imshow(week_2km.isel(time = 14).T_2M.values[:500,:500])
ax1.set_title('Fine resolution target image')
ax2.imshow(di_coarse[:500,:500], norm =norm)
#ax2.imshow(di_coarse[:500,:500])
ax2.set_title('Coarse resolution target image')
#dt consists of two zeros representing two continuous variables
dt = [0]*ti.shape[-1]

simulation,index,_=g2s('-a', 'qs', '-submitOnly', '-sa', 'g2s.dcsr.unil.ch', '-ti',ti, '-di',di, '-dt',dt, '-k',1.2, '-n',50, '-j',0.5)
#simulation,index,_=g2s('-a', 'qs', '-ti',ti, '-di',di, '-dt',dt, '-k',1.2, '-n',50, '-j',0.5)


norm =colors.Normalize(vmin=ti_T.min(),vmax=ti_T.max())
f,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(12,12),sharex=True,sharey=True)
plt.subplots_adjust(wspace=0.1,hspace=0.1)
plt.suptitle('QS Downscaling',size='xx-large')
ax1.imshow(di_coarse[:500,:500],norm=norm)
ax1.set_title('Coarse res di')
ax2.imshow(simulation[:,:,0], norm =norm)
ax2.set_title('Simulation')
ax3.imshow(index)
ax3.set_title('Index')
ax4.imshow(ti_T[:500,:500],norm=norm)
ax4.set_title('True image')


norm =colors.Normalize(vmin=ti_T.min(),vmax=ti_T.max())
f,(ax1,ax2) = plt.subplots(2,1,figsize=(12,12))
ax1.imshow(week_2km.isel(time = 17).T_2M.values[:500,:500], norm =norm)
ax1.set_title('Fine resolution target image')
ax2.imshow(simulation[:,:,0], norm =norm)
#ax2.imshow(simulation[:,:,0])
ax2.set_title('Coarse resolution target image')