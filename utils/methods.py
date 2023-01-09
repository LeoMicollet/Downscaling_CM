import numpy as np
from matplotlib import pyplot as plt
import xarray as xr
import pandas as pd
from sklearn.linear_model import LinearRegression

def getliste_X(mat): 
    liste = list()
    print(mat.shape)
    for t in range(mat.shape[0]):
        for i in range(0, mat.shape[:-1,:-1][1], 2):
            print(i)
            liste.append(mat[t][:,i:i+2])
    return tuple(liste)

def getliste_Y(mat): 
    liste = list()
    for t in range(mat.shape[0]):
        for i in range(0, mat.shape[1], 12):
            liste.append(mat[t][:,i:i+12]) = liste + (mat[t][i:i+12])
    return liste