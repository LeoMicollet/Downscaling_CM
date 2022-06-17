import os
import numpy as np
from scipy.interpolate import interpolate
import xarray as xr
import xesmf as xe
#, ofile, ingrid, outgrid

def create_grid(lon_min, lon_max, lon_dim, lat_min, lat_max, lat_dim) : # Creates a grid with lat/lon and limits  to the grid (only used for conservative remapping)
    grid = xr.Dataset(
        {
            "lon": (["lon"], np.arange(lon_min, lon_max, lon_dim)),
            "lat": (["lat"], np.arange(lat_min, lat_max, lat_dim)),
            "lon_b": (["lon_b"], np.arange(lon_min, lon_max + lon_dim, lon_dim)),
            "lat_b": (["lat_b"], np.arange(lat_min, lat_max + lat_dim, lat_dim)),
        }
    )
    return grid

def upscale(ds, ingrid, outgrid) : # Concervative remaping is used (mean between pixels)
    ups_grid = xe.Regridder(ingrid, outgrid, "conservative")
    ups = ups_grid(ds)
    ups = ups.rename({'lon': 'rlon','lat': 'rlat'})
    return ups

def downscale(in_ds, target_ds, lon_min, lon_max, lon_dim, lat_min, lat_max, lat_dim, new_lon_max, new_lon_dim, new_lat_max, new_lat_dim, interp_type): 
    #target_ds must be a dataset with the dimensions we want, and the same variables. It will be overwritten 
    # interp_type could be {'linear', 'cubic', 'quintic'}
    lon = np.arange(lon_min, lon_max, lon_dim)
    lat = np.arange(lat_min, lat_max, lat_dim)
    for j in range(len(in_ds.time)) :
        part_ds =in_ds.isel(time = j)
        time = list(in_ds["time"])
        
        # Temperature interpolation
        fun = interpolate.interp2d(lon, lat, part_ds.T_2M, kind=interp_type) 
        newlon = np.arange(lon_min, new_lon_max, new_lon_dim)
        newlat = np.arange(lat_min, new_lat_max, new_lat_dim)
        newvar = fun(newlon, newlat)
        target_ds.T_2M.loc[dict(time = time[j])] = newvar
        
        # Total precipitation interpolation
        fun = interpolate.interp2d(lon, lat, part_ds.TOT_PR, kind=interp_type)
        newlon = np.arange(lon_min, new_lon_max, new_lon_dim)
        newlat = np.arange(lat_min, new_lat_max, new_lat_dim)
        newvar = fun(newlon, newlat)
        target_ds.TOT_PR.loc[dict(time = time[j])] = newvar
        
        # Relative humidity interpolation
        fun = interpolate.interp2d(lon, lat, part_ds.RELHUM_2M, kind=interp_type)
        newlon = np.arange(lon_min, new_lon_max, new_lon_dim)
        newlat = np.arange(lat_min, new_lat_max, new_lat_dim)
        newvar = fun(newlon, newlat)
        target_ds.RELHUM_2M.loc[dict(time = time[j])] = newvar        
    return target_ds
