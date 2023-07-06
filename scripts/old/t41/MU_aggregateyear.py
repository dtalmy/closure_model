# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 09:02:00 2022

@author: eric
"""
import sys
import argparse
import cartopy
import pandas as pd
import xarray as xr
import datetime
import numpy as np
import os 
import geopandas as gpd
from shapely.geometry import Point
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import dask.dataframe as dd
import pathlib




def main():
    print(args.DIRnc, file = sys.stdout)
    
    filedir=args.DIRnc
    P_run  =pathlib.Path(filedir)
    if P_run.exists():
        print('Model Run Dir exists :'+ P_run.as_posix(), file = sys.stdout)
        os.chdir(P_run)
        Print('Current working dir set to: ' + Path.cwd(), file = sys.stdout )
    else:
        sys.exit('Model run Dir does not exist :'+ P_run.as_posix())
    #    
    P_nc   =pathlib.Path(filedir+'/NC_trace')
    if P_nc.exists():
        print('Model NC Dir exists :'+ P_nc.as_posix(), file = sys.stdout)
    else:
        sys.exit('Model NC Dir does not exist :'+ P_nc.as_posix())
    #    
    P_anal = pathlib.Path(filedir+'/NC_anal')
    P_anal.mkdir(parents=True, exist_ok=True)
    
    ext_deps_all=[-5.0000e+00, -1.5000e+01, -2.7500e+01, -4.5000e+01, -6.5000e+01, -8.7500e+01, -1.1750e+02, -1.6000e+02]
    month_list=[1,2,3,4,5,6,7,8,9,10,11,12]
    bact_list=['C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20']
    virus_list=['C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 
            'C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C37', 'C38', 'C39', 'C40']

    
    NC_fileptracer=[\
        'ptracers.c01.v4c.nc' , \
        'ptracers.c02.v4c.nc' , \
        'ptracers.c03.v4c.nc' , \
        'ptracers.c04.v4c.nc' , \
        'ptracers.c05.v4c.nc' , \
        'ptracers.c06.v4c.nc' , \
        'ptracers.c07.v4c.nc' , \
        'ptracers.c08.v4c.nc' , \
        'ptracers.c09.v4c.nc' , \
        'ptracers.c10.v4c.nc' , \
        'ptracers.c11.v4c.nc' , \
        'ptracers.c12.v4c.nc' , \
        'ptracers.c13.v4c.nc' , \
        'ptracers.c14.v4c.nc' , \
        'ptracers.c15.v4c.nc' , \
        'ptracers.c16.v4c.nc' , \
        'ptracers.c17.v4c.nc' , \
        'ptracers.c18.v4c.nc' , \
        'ptracers.c19.v4c.nc' , \
        'ptracers.c20.v4c.nc' , \
        'ptracers.c21.v4c.nc' , \
        'ptracers.c22.v4c.nc' , \
        'ptracers.c23.v4c.nc' , \
        'ptracers.c24.v4c.nc' , \
        'ptracers.c25.v4c.nc' , \
        'ptracers.c26.v4c.nc' , \
        'ptracers.c27.v4c.nc' , \
        'ptracers.c28.v4c.nc' , \
        'ptracers.c29.v4c.nc' , \
        'ptracers.c30.v4c.nc' , \
        'ptracers.c31.v4c.nc' , \
        'ptracers.c32.v4c.nc' , \
        'ptracers.c33.v4c.nc' , \
        'ptracers.c34.v4c.nc' , \
        'ptracers.c35.v4c.nc' , \
        'ptracers.c36.v4c.nc' , \
        'ptracers.c37.v4c.nc' , \
        'ptracers.c38.v4c.nc' , \
        'ptracers.c39.v4c.nc' , \
        'ptracers.c40.v4c.nc' , \
        'ptracers.c41.v4c.nc' , \
        'ptracers.ALK.v4c.nc' , \
        'ptracers.DIC.v4c.nc' , \
        'ptracers.DOC.v4c.nc' , \
        'ptracers.DOFe.v4c.nc' , \
        'ptracers.DON.v4c.nc' , \
        'ptracers.DOP.v4c.nc' , \
        'ptracers.FeT.v4c.nc' , \
        'ptracers.NH4.v4c.nc' , \
        'ptracers.NO2.v4c.nc' , \
        'ptracers.NO3.v4c.nc' , \
        'ptracers.O2.v4c.nc' , \
        'ptracers.PIC.v4c.nc' , \
        'ptracers.PO4.v4c.nc' , \
        'ptracers.POC.v4c.nc' , \
        'ptracers.POFe.v4c.nc' , \
        'ptracers.PON.v4c.nc' , \
        'ptracers.POP.v4c.nc' , \
        'ptracers.POSi.v4c.nc' , \
        'ptracers.SiO2.v4c.nc' \
            ]
    #
    # Create Phyto file
    NC_phytofiles=NC_fileptracer[0:10]  
    
    
    
    ds_tracers=xr.open_mfdataset(NC_phytofiles,  combine='by_coords', parallel=False)
    #
    # limit time
    #time - use 2nd to last year
    #last year is not a complete 12 months
    #find 2nd to last year
    print('Limit year  :: start', flush=True, file = sys.stdout)
    tempdate=ds_tracers.T.max()
    YEAR_index=int(tempdate.T.dt.year)-1
    #YEAR_index
    ds_tracers=ds_tracers.isel(T=(ds_tracers.T.dt.year == YEAR_index))
    #
    #limit depth
    print('Limit depth  :: start', flush=True, file = sys.stdout)
    # #print(ds_tracers.dims, flush=True, file = sys.stdout)
    #ds_tracers=ds_tracers.loc[dict(Z=ext_deps)]
    ds_tracers=ds_tracers.isel(Z=(ds_tracers.Z > (min(ext_deps_all)-1) ) )
    #
    ds_phyto['small_phyto']= \
      ds_tracers['c06'] \
    + ds_tracers['c07'] + ds_tracers['c08']+ ds_tracers['c09'] \
    + ds_tracers['c10']
    
    ds_phyto['large_phyto']= \
      ds_tracers['c01'] + ds_tracers['c02']+ ds_tracers['c03'] \
    + ds_tracers['c04'] + ds_tracers['c05']
    file_phyto=P_nc.joinpath('phyto.nc')
    ds_phyto.to_netcdf(file_phyto)
    
    
    
#
if __name__ == "__main__":
    main()
    #Initialize
    parser=argparse.ArgumentParser(description="Extract 1 year and aggregate NC files ,write resutls")
     
    #Adding optional parameters
     
    parser.add_argument('-D',
                        '--DIRnc',
                        help="Dir of netcdf files",
                        required=True,
                        type=str)
 
    args = parser.parse_args()
    main()