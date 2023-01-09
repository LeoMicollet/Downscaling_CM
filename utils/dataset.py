import xarray as xr
import numpy as np
import os
import glob
from matplotlib import pyplot as plt

def getfiles() :
    """
    Creates a list with all the file names.

    Returns:
        filenames: A list conatining all the file names.
    """
  
    filenames  = glob.glob("lffd*")
    filenames = sorted(filenames)
    return filenames

def summer_ds(fnames) :
    """
    Creates a new dataset containing all the values during the summer.
  
    Parameters:
        fnames: list with the names of each files.
          
    Returns:
        summer_dataset: netCDF dataset containing all the summer values.
    """
  
    summer = [xr.open_dataset(file) for file in fnames[172*24:265*24]]
    sorted_summer = [xr.merge([file.T_2M, file.RELHUM_2M, file.TOT_PR]) for file in summer]
    summer_dataset = xr.concat(sorted_summer, dim='time')
    return summer_dataset

#winter_ds not working
def winter_ds(fnames) : 
    """
    Creates a new dataset containing all the values during the winter.
  
    Parameters:
        fnames: list with the names of each files.
          
    Returns:
        winter_dataset: netCDF dataset containing all the winter values.
    """
    
    winter = [xr.open_dataset(file) for file in [fnames[:80*24] + fnames[356*24:]]]
    sorted_winter = [xr.merge([file.T_2M, file.RELHUM_2M, file.TOT_PR]) for file in winter]
    winter_dataset = xr.concat(sorted_winter, dim='time')
    return winter_dataset

def new_dataset(fnames, first_day, last_day) : # Create a new dataset containing all the values between first and last day
    """
    Creates a new dataset containing all the values between a given first and last day.
  
    Parameters:
        fnames: list with the names of each files.
        
        first_day: the first day on which the values will be taken
        
        last_day: the last day on which the values will be taken
          
    Returns:
        dataset: netCDF dataset containing all the chosen values.
    """
    
    fd = first_day*24
    ld = last_day*24
    dataset = [xr.open_dataset(file) for file in fnames[fd:ld]]
    sorted_ds = [xr.merge([file.T_2M, file.RELHUM_2M, file.TOT_PR]) for file in dataset]
    dataset = xr.concat(sorted_ds, dim='time')
    return dataset

def empty_dataset(ds, val) :
    """
    Creates a new dataset containing only val, the same size as a already existing dataset.
  
    Parameters:
        ds: dataset the size we want to create.
        
        val: the value chosen to be put in the new dataset
          
    Returns:
        dataset: netCDF dataset containing only val.
    """
        
    if(val == None):
        return 0
    else:
        empty_ds = xr.full_like(ds, val)
    return empty_ds

def save_dataset(ds, name) : # Saves the dataset
    """
    Saves the dataset under the filename name.
  
    Parameters:
        ds: Dataset that will be saved.
        
        name: Name of the saved dataset
    """
    
    path = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/Downscaling_CM/data"
    os.chdir(path)
    filename = './'+name+'.nc'
    print ('saving to ', filename)
    ds.to_netcdf(path=filename)
    ds.close()
    print ('finished saving')
    
def get_training_set(filenames):
    """
    Creates and saves training dataset.
  
    Parameters:
        filenames: list with the names of each files.
          
    Returns:
        training_ds: netCDF dataset containing all the values from the first 2 weeks of each month.
    """
    
    names = []
    month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    two_weeks = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']
    for m in month :
        for d in two_weeks :
            for name in filenames :
                if name.startswith('lffd2003'+m+d): 
                    names.append(name)
    print(int(len(names)/24))
    training_ds = new_dataset(names, 0, int(len(names)/24))
    save_dataset(training_ds, 'training_ds')
    return training_ds
    
def get_validation_set(filenames):
    """
    Creates and saves validation dataset.
  
    Parameters:
        filenames: list with the names of each files.
          
    Returns:
        validation_ds: netCDF dataset containing all the values from the third week of each month.
    """
    
    names = []
    month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    third_week = ['15', '16', '17', '18', '19', '20', '21']
    for m in month :
        for d in third_week :
            for name in filenames :
                if name.startswith('lffd2003'+m+d): 
                    names.append(name)
    validation_ds = new_dataset(names, 0, int(len(names)/24))
    save_dataset(validation_ds, 'validation_ds')
    return validation_ds
    
def get_testing_set(filenames):
    """
    Creates and saves testing dataset.
  
    Parameters:
        filenames: list with the names of each files.
          
    Returns:
        training_ds: netCDF dataset containing all the values from the last weeks of each month.
    """
    
    names = []
    month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    last_week = ['22', '23', '24', '25', '26', '27', '28', '29','30', '31']
    for m in month :
        for d in last_week :
            for name in filenames :
                if name.startswith('lffd2003'+m+d): 
                    names.append(name)
    testing_ds = new_dataset(names, 0, int(len(names)/24))
    save_dataset(testing_ds, 'testing_ds')
    return testing_ds