import os
#, ofile, ingrid, outgrid
def upscale(ds, infile) :
    filename = './'+infile+'.nc'
    ds.to_netcdf(path=filename)
    ds.close()
    print("Dataset saved as ", infile)
    cdo remapcon,same_dim_grid.txt -setgrid,CLM_lm_f_grid.txt random_week_2km.nc random_week_12km.nc
    list_files = subprocess.run(["remapcon,"same_dim_grid.txt" -setgrid,"CLM_lm_f_grid.txt" "random_week_2km.nc" "random_week_12km.nc)
    print("Upscaled file saved as ", ofile)
    return -1