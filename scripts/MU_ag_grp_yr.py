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


ext_deps_all=[-5.0000e+00, -1.5000e+01, -2.7500e+01, -4.5000e+01, -6.5000e+01, -8.7500e+01, -1.1750e+02, -1.6000e+02]
month_list=[1,2,3,4,5,6,7,8,9,10,11,12]
filedir='E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1D'
#bact_list=['C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20']
#virus_list=['C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C37', 'C38', 'C39', 'C40']
#
# Difficult to figure out how to make this generic to handle different number of tracers.
# set this up to edit these global list for each of the groups we are using
# Thisrequires 2 list; one for files; one for names
#                        D  l  s  P  T  C  AP AD NP ND B  V   Z   
#grp_nplank(:)=          0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 20, 1,
#vars_to_sum = ["a", "c", "d"]
#summed_variables = ds[vars_to_sum].isel(y=-1).to_array().sum("variable")
#
NC_file_l=[\
    'ptracers.c01.v4c.nc' ]
vars_to_sum_l = ['c01']  
#  
NC_file_s=[\
    'ptracers.c02.v4c.nc' ]
vars_to_sum_s = ['c02']  
# 
NC_file_AP=[ ]  
vars_to_sum_AP = []  
# 
NC_file_AD=[ ]
vars_to_sum_AD = []  
# 
NC_file_V=[ ]
vars_to_sum_V = []  
# 
NC_file_Z=[\
    'ptracers.c03.v4c.nc' ]
vars_to_sum_Z = ['c03']  
#
NC_file_nutr=[\
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
# full 41 list for reference      
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



def main():
    print(args.DIRmrun, file = sys.stdout)
    
    filedir=args.DIRmrun
    P_run  =pathlib.Path(filedir)
    if P_run.exists():
        print('Model Run Dir exists :'+ P_run.as_posix(), file = sys.stdout)
        os.chdir(P_run)
        P_wd=pathlib.Path.cwd()
        print('Current working dir set to: ' + P_wd.as_posix(), file = sys.stdout )
    else:
        sys.exit('Model run Dir does not exist :'+ P_run.as_posix())
    #    
    P_nc   =pathlib.Path(filedir+'/NC_trace')
    if P_nc.exists():
        print('Model NC Dir exists :'+ P_nc.as_posix(), file = sys.stdout)
    else:
        sys.exit('Model NC Dir does not exist :'+ P_nc.as_posix())
    #    
    P_anal = pathlib.Path(filedir+'/NC_analysis')
    P_anal.mkdir(parents=True, exist_ok=True)

    
    #
    # I amprocessing these in groups to try to limit the number loaded at any one time
    #                        D  l  s  P  T  C  AP AD NP ND B  V   Z   
    #grp_nplank(:)=          0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 20, 1,
    #
    # Create Phyto file
    # NC_phytofiles=NC_fileptracer[0:10] 
    # NC_bactfiles=NC_fileptracer[10:20]  
    # NC_virusfiles=NC_fileptracer[20:40] 
    # NC_zoofiles=NC_fileptracer[40]
    # NC_otherfiles=NC_fileptracer[41:60]
    #
    os.chdir(P_nc)
    P_wd=pathlib.Path.cwd()
    print('Current working dir set to: ' + P_wd.as_posix(), file = sys.stdout )
    #
    # process l
    NC_file     =NC_file_l
    vars_to_sum =vars_to_sum_l 
    if len(NC_file)>0:
        ds_tracers=xr.open_mfdataset(NC_file,  combine='by_coords', parallel=False)
        #
        # limit time
        #time - use 2nd to last year
        #last year is not a complete 12 months
        #find 2nd to last year
        print('large_phyto : Limit year  :: start', flush=True, file = sys.stdout)
        tempdate=ds_tracers.T.max()
        YEAR_index=int(tempdate.T.dt.year)-1
        #YEAR_index
        ds_tracers=ds_tracers.isel(T=(ds_tracers.T.dt.year == YEAR_index))
        #
        #limit depth
        print('large_phyto : Limit depth  :: start', flush=True, file = sys.stdout)
        # #print(ds_tracers.dims, flush=True, file = sys.stdout)
        #ds_tracers=ds_tracers.loc[dict(Z=ext_deps)]
        ds_tracers=ds_tracers.isel(Z=(ds_tracers.Z > (min(ext_deps_all)-1) ) )
        #
        #
        print('large_phyto : process  :: start', flush=True, file = sys.stdout)
        #
        ds_tracers['large_phyto']= xr.zeros_like(ds_tracers[vars_to_sum[0]])
        for var in  vars_to_sum:
            ds_tracers['large_phyto'] = ds_tracers['large_phyto'] + ds_tracers[var]
        #ds_tracers['large_phyto']= ds_tracers[vars_to_sum].isel(y=-1).to_array().sum("variable")
        #
        # use copy to create new dataarray with variable data, etc. FOR FIRST AGGREGATE
        ds_anal=ds_tracers['large_phyto'].copy()
        ds_tracers.close()
    #
    # process s
    NC_file     =NC_file_s
    vars_to_sum =vars_to_sum_s 
    if len(NC_file)>0:
        ds_tracers=xr.open_mfdataset(NC_file,  combine='by_coords', parallel=False)
        #
        # limit time
        #time - use 2nd to last year
        #last year is not a complete 12 months
        #find 2nd to last year
        print('small_phyto : Limit year  :: start', flush=True, file = sys.stdout)
        tempdate=ds_tracers.T.max()
        YEAR_index=int(tempdate.T.dt.year)-1
        #YEAR_index
        ds_tracers=ds_tracers.isel(T=(ds_tracers.T.dt.year == YEAR_index))
        #
        #limit depth
        print('small_phyto : Limit depth  :: start', flush=True, file = sys.stdout)
        # #print(ds_tracers.dims, flush=True, file = sys.stdout)
        #ds_tracers=ds_tracers.loc[dict(Z=ext_deps)]
        ds_tracers=ds_tracers.isel(Z=(ds_tracers.Z > (min(ext_deps_all)-1) ) )
        #
        print('small_phyto : process  :: start', flush=True, file = sys.stdout)
        #
        #
        ds_tracers['small_phyto']= xr.zeros_like(ds_tracers[vars_to_sum[0]])
        for var in  vars_to_sum:
            ds_tracers['small_phyto'] = ds_tracers['small_phyto'] + ds_tracers[var]
        # use copy to create new dataarray with variable data, etc. FOR FIRST AGGREGATE
        ds_anal= xr.merge([ds_anal,ds_tracers['small_phyto']])
        ds_tracers.close()
    #
    # process AP
    print('AP : Zero ENTRY  :: start', flush=True, file = sys.stdout)
    ds_anal['AP']= xr.zeros_like(ds_anal['large_phyto'])
    #
    # process AD
    print('AD : Zero ENTRY  :: start', flush=True, file = sys.stdout)
    ds_anal['AD']= xr.zeros_like(ds_anal['large_phyto'])
    #
    # process VIRUS
    print('virus : Zero ENTRY  :: start', flush=True, file = sys.stdout)
    ds_anal['virus']= xr.zeros_like(ds_anal['large_phyto'])
    #
    # process Z
    NC_file     =NC_file_Z
    vars_to_sum =vars_to_sum_Z 
    if len(NC_file)>0:
        ds_tracers=xr.open_mfdataset(NC_file,  combine='by_coords', parallel=False)
        #
        # limit time
        #time - use 2nd to last year
        #last year is not a complete 12 months
        #find 2nd to last year
        print('zoo : Limit year  :: start', flush=True, file = sys.stdout)
        tempdate=ds_tracers.T.max()
        YEAR_index=int(tempdate.T.dt.year)-1
        #YEAR_index
        ds_tracers=ds_tracers.isel(T=(ds_tracers.T.dt.year == YEAR_index))
        #
        #limit depth
        print('zoo : Limit depth  :: start', flush=True, file = sys.stdout)
        # #print(ds_tracers.dims, flush=True, file = sys.stdout)
        #ds_tracers=ds_tracers.loc[dict(Z=ext_deps)]
        ds_tracers=ds_tracers.isel(Z=(ds_tracers.Z > (min(ext_deps_all)-1) ) )
        #
        #
        print('zoo : process  :: start', flush=True, file = sys.stdout)
        #
        ds_tracers['zoo']= xr.zeros_like(ds_tracers[vars_to_sum[0]])
        for var in  vars_to_sum:
            ds_tracers['zoo'] = ds_tracers['zoo'] + ds_tracers[var]
        # use copy to create new dataarray with variable data, etc. FOR FIRST AGGREGATE
        ds_anal= xr.merge([ds_anal,ds_tracers['zoo']])
        ds_tracers.close()
    #
    # process nutr
    NC_file     =NC_file_nutr
    #vars_to_sum =vars_to_sum_Z 
    if len(NC_file)>0:
        ds_tracers=xr.open_mfdataset(NC_file,  combine='by_coords', parallel=False)
        #
        # limit time
        #time - use 2nd to last year
        #last year is not a complete 12 months
        #find 2nd to last year
        print('nutr : Limit year  :: start', flush=True, file = sys.stdout)
        tempdate=ds_tracers.T.max()
        YEAR_index=int(tempdate.T.dt.year)-1
        #YEAR_index
        ds_tracers=ds_tracers.isel(T=(ds_tracers.T.dt.year == YEAR_index))
        #
        #limit depth
        print('nutr : Limit depth  :: start', flush=True, file = sys.stdout)
        # #print(ds_tracers.dims, flush=True, file = sys.stdout)
        #ds_tracers=ds_tracers.loc[dict(Z=ext_deps)]
        ds_tracers=ds_tracers.isel(Z=(ds_tracers.Z > (min(ext_deps_all)-1) ) )
        #
        print('nutr : process  :: start', flush=True, file = sys.stdout)
        #
        ds_anal= xr.merge([ds_anal,ds_tracers['DOC']])
        ds_anal= xr.merge([ds_anal,ds_tracers['POC']])
        ds_anal= xr.merge([ds_anal,ds_tracers['DIC']])
        ds_anal= xr.merge([ds_anal,ds_tracers['DOP']])
        ds_anal= xr.merge([ds_anal,ds_tracers['DOFe']])
        ds_tracers.close()
    #
    #save file
    file_phyto=P_nc.joinpath('GRPD_yr.nc')
    print(file_phyto)
    ds_anal.to_netcdf(file_phyto,format="NETCDF4")    
    
#
if __name__ == "__main__":
    #Initialize
    parser=argparse.ArgumentParser(description="Extract 1 year and aggregate NC files ,write resutls")
     
    #Adding optional parameters
     
    parser.add_argument('-MD',
                        '--DIRmrun',
                        help="Base Dir of model run",
                        required=True,
                        type=str)
 
    args = parser.parse_args()
    main()