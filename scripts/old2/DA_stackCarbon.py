# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 15:39:18 2022

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
from pylr2 import regress2
from matplotlib.font_manager import FontProperties
import matplotlib.gridspec as gridspec
import cartopy.feature as cfeature
import cartopy.crs as ccrs

ext_deps_all=[-5.0000e+00, -1.5000e+01, -2.7500e+01, -4.5000e+01, -6.5000e+01, -8.7500e+01, -1.1750e+02, -1.6000e+02]
month_list=[1,2,3,4,5,6,7,8,9,10,11,12]
PD_NC=pathlib.Path('E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1D_long_59771\\NC_trace')
# #PD_NC=pathlib.Path('E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1Dmay5\\NC_trace')
PD_out=pathlib.Path('E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1D_long_59771\\NC_analysis')
tag='59771_'
NC_file=[\
    'ptracers.c01.v4c.nc', \
    'ptracers.c02.v4c.nc', \
    'ptracers.c03.v4c.nc', \
    'grid.v4c.nc'          \
    ]
L_tracer=[\
    'c01', \
    'c02', \
    'c03'  \
    ]


def multi_stackCarbon(PD_NC,tag,PD_out):
    #
    #
    os.chdir(PD_NC)
    P_wd=pathlib.Path.cwd()
    print('Current working dir set to: ' + P_wd.as_posix(), file = sys.stdout )
    #
    filename=tag+str('_stackCarbon.png')
    file_out=PD_out.joinpath(filename)
    ds_tracers=xr.open_mfdataset(NC_file,  combine='by_coords', parallel=False)
    #
    # limit time
    #time - use  last year 3 years
    print('Limit year  :: start', flush=True, file = sys.stdout)
    tempdate=ds_tracers.T.max()
    YEAR_index=int(tempdate.T.dt.year)
    ds_tracers=ds_tracers.isel(T=(ds_tracers.T.dt.year >= YEAR_index-2))
    #
    #limit depth 
    print('Limit depth  :: start', flush=True, file = sys.stdout)
    # #print(ds_tracers.dims, flush=True, file = sys.stdout)
    #ds_tracers=ds_tracers.loc[dict(Z=ext_deps)]
    ds_tracers=ds_tracers.isel(Z=(ds_tracers.Z > (min(ext_deps_all)-1) ) )
    #
    #ds_tracers['Depth'].plot()
    # Identify areas that are not modeled over and remove 
    ds_tracers['bathy_mask']=ds_tracers['Depth'].where(ds_tracers['Depth'] != 0)  
    #ds_tracers['bathy_mask'].plot()
    #ds_tracers['c01'].isel(T=0, Z=0).plot()
    ds_tracers=ds_tracers.where(ds_tracers['Depth'] != 0) 
    #
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ds_tracers['c01'].isel(T=0, Z=0).plot(ax=ax)
    ax.set_title('Implemented Mask')
    fig.tight_layout()
    filename=tag+str('_m_mask.png')
    file_out=PD_out.joinpath(filename)
    fig.savefig(file_out,dpi=300, bbox_inches='tight')
    plt.show()    
    #
    # Sum selected depths
    #ds_tracers=ds_tracers.sum(dim='Z')
    #
    #average
    #ds_tracers
    #ds_time=ds_tracers.sum(dim=["X", "Y","Z"])
    # ds_tracers['c01_mean']=ds_tracers['c01'].mean(dim=["T","Z"])
    # ds_tracers['c01_var']=ds_tracers['c01'].var(dim=["T","Z"])
    # ds_tracers['c01_stddev']=ds_tracers['c01_var']**(1/2)
    # ds_tracers['c01_max']=ds_tracers['c01'].max(dim=["T","Z"])
    # ds_tracers['c01_min']=ds_tracers['c01'].min(dim=["T","Z"])
    # plt.scatter(ds_tracers['c01_mean'],ds_tracers['c01_var'])
    # #Coefficient of variation
    # ds_tracers['c01_coefvar']=ds_tracers['c01_var']/ds_tracers['c01_mean']
    # ds_tracers['c01_coefvar'].plot()
    
    # ds_tracers['c01_max'].plot()
    # #
    # #
    # ds_tracers['c02_mean']=ds_tracers['c02'].mean(dim=["T","Z"])
    # ds_tracers['c02_var']=ds_tracers['c02'].var(dim=["T","Z"])
    # ds_tracers['c02_stddev']=ds_tracers['c02_var']**(1/2)
    # ds_tracers['c02_max']=ds_tracers['c02'].max(dim=["T","Z"])
    # ds_tracers['c02_min']=ds_tracers['c02'].min(dim=["T","Z"])
    # plt.scatter(ds_tracers['c02_mean'],ds_tracers['c02_var'])
    # #Coefficient of variation
    # ds_tracers['c02_coefvar']=ds_tracers['c02_var']/ds_tracers['c02_mean']
    # ds_tracers['c02_coefvar'].plot()
    
    # ds_tracers['c02_max'].plot()
    # #
    # #
    # #
    # #
    # s_trace=str('c01')
    # s_trace=str('c03')
    # s_trace=str('c03')
    #
    #plt.plot(ds_tracers['T'],ds_tracers['c02'].mean(dim=["X","Y","Z"]))
    fig, ax = plt.subplots(nrows=1, ncols=1)
    for trace in L_tracer:
        s_trace=str(trace)
        ax.plot(ds_tracers['T'],ds_tracers[s_trace].mean(dim=["X","Y","Z"]),label=s_trace)
    ax.legend(loc=(1.04,0))
    ax.set_title('c01-3 global mean values at timestep')
    fig.tight_layout()
    filename=tag+str('_lg_globmean.png')
    file_out=PD_out.joinpath(filename)
    fig.savefig(file_out,dpi=300, bbox_inches='tight')
    plt.show()    
    #
    ds_tracers['tot']=ds_tracers['c01']+ds_tracers['c02']+ds_tracers['c03']
    maxtest=ds_tracers['tot'].max(dim=["T","Z"],keep_attrs=True)
   # gb_zmean=ds_tracers.mean(dim=["Z"])
   # gb_max=gb_zmean.groupby('tot').max()
    for trace in L_tracer:
        
        s_trace=str(trace)
        print('Plot trace : ' +s_trace, file = sys.stdout)
        ds_tracers[s_trace+'_mean']=ds_tracers[s_trace+''].mean(dim=["T","Z"])
        ds_tracers[s_trace+'_var']=ds_tracers[s_trace+''].var(dim=["T","Z"])
        ds_tracers[s_trace+'_stddev']=ds_tracers[s_trace+'_var']**(1/2)
        ds_tracers[s_trace+'_max']=ds_tracers[s_trace+''].max(dim=["T","Z"])
        ds_tracers[s_trace+'_min']=ds_tracers[s_trace+''].min(dim=["T","Z"])
        
        #Coefficient of variation
        ds_tracers[s_trace+'_coefvar']=ds_tracers[s_trace+'_stddev']/ds_tracers[s_trace+'_mean']
        #ds_tracers[s_trace+'_coefvar'].plot()
        
        #ds_tracers[s_trace+'_max'].plot()
        #
        #
        #fig ,[ax1,ax2]= plt.subplots(nrows=2, ncols=1)
        fig = plt.figure(figsize=[18, 18])
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2, projection=ccrs.Mollweide())
        #ax1 = plt.gca()
        ax1.scatter(ds_tracers[s_trace+'_mean'] ,ds_tracers[s_trace+'_stddev'] , c='blue', alpha=0.05, edgecolors='none')
        #ax1.set_yscale('log')
        #ax1.set_xscale('log')
        ax1.set_xlabel('mean',fontsize=30)
        ax1.set_ylabel('Std. Dev.',fontsize=30)
        #
        ax2.set_global()
        ax2.set_title('Coeff of Variation')
        #possible projection issue
        ds_tracers[s_trace+'_coefvar'].plot(transform=ccrs.PlateCarree(),ax=ax2)
        #ds_tracers[s_trace+'_coefvar'].plot(transform=ccrs.Geodetic(),ax=ax2)
        #
        fig.suptitle(s_trace, fontsize=40)
        fig.tight_layout()
        filename=tag+s_trace+str('_coefvar.png')
        file_out=PD_out.joinpath(filename)
        fig.savefig(file_out,dpi=300, bbox_inches='tight')
        plt.show()    
    #
    #stack plot
    #
    # ds_tracers['c_tot']=ds_tracers['c01_mean']+ds_tracers['c02_mean']+ds_tracers['c03_mean']
    # ds_tracers['phyto_mean']=ds_tracers['c01_mean']+ds_tracers['c02_mean']
    # ds_tracers['zoo_mean']=ds_tracers['c03_mean']
    # ds_tracers['zp_mean']=ds_tracers['zoo_mean']/ds_tracers['phyto_mean']
    # #
    # fig, ax = plt.subplots()
    # ax.scatter(ds_tracers['c_tot'],ds_tracers['c02_mean'], c='blue',label='small phyto')
    # ax.scatter(ds_tracers['c_tot'],ds_tracers['c01_mean']+ds_tracers['c02_mean'],c='green',label='large phyto')
    # ax.scatter(ds_tracers['c_tot'],ds_tracers['c01_mean']+ds_tracers['c02_mean']+ds_tracers['c03_mean'], c='red',label='zooplankton')
    # ax.set_title('Mean value over time and depth')
    # ax.set_xlabel('Total of ind. Planktonics C (mmol C/m^3)')
    # ax.set_ylabel('Size fracionated C (mmol C/m^3)')
    # ax.legend(loc=(1.04,0))
    # ax2 = ax.twinx()
    # color = 'tab:red'
    # ax2.set_ylabel('mean zp ratio', color=color)
    # ax2.scatter(ds_tracers['c_tot'],ds_tracers['zp_mean'], c='blue',label='small phyto')
    # fig.tight_layout()
    # filename=tag+str('_.png')
    # file_out=PD_out.joinpath(filename)
    # fig.savefig(file_out,dpi=300, bbox_inches='tight')
    # plt.show() 
    #
    #stack plot
    #
    L_suffix=[str('max'),str('mean'),str('min')]
    #suffix=str('max')
    #suffix=str('mean')
    for suffix in L_suffix:
        s_suffix=str('_')+suffix
        ds_tracers['c_tot'+s_suffix]=ds_tracers['c01'+s_suffix]+ds_tracers['c02'+s_suffix]+ds_tracers['c03'+s_suffix]
        ds_tracers['phyto'+s_suffix]=ds_tracers['c01'+s_suffix]+ds_tracers['c02'+s_suffix]
        ds_tracers['zoo'+s_suffix]=ds_tracers['c03'+s_suffix]
        ds_tracers['zp'+s_suffix]=ds_tracers['zoo'+s_suffix]/ds_tracers['phyto'+s_suffix]
        #
        fig, ax = plt.subplots()
        ax.scatter(ds_tracers['c_tot'+s_suffix],ds_tracers['c02'+s_suffix], c='blue',label='small phyto')
        ax.scatter(ds_tracers['c_tot'+s_suffix],ds_tracers['c01'+s_suffix]+ds_tracers['c02'+s_suffix],c='green',label='large phyto')
        ax.scatter(ds_tracers['c_tot'+s_suffix],ds_tracers['c01'+s_suffix]+ds_tracers['c02'+s_suffix]+ds_tracers['c03'+s_suffix], c='red',label='zooplankton')
        ax.set_title(suffix +' value over time and depth')
        ax.set_xlabel('Total of ind. Planktonics C (mmol C/m^3)')
        ax.set_ylabel('Size fracionated C (mmol C/m^3)')
        ax.legend(loc=(1.04,0))
        ax2 = ax.twinx()
        color = 'tab:gray'
        ax2.set_ylabel(suffix +' zp ratio', color=color)
        ax2.scatter(ds_tracers['c_tot'+s_suffix],ds_tracers['zp'+s_suffix], alpha=0.5, facecolors='none', edgecolors=color,label='Z:P')
        fig.tight_layout()
        filename=tag+str('_')+suffix+str('_stack.png')
        file_out=PD_out.joinpath(filename)
        fig.savefig(file_out,dpi=300, bbox_inches='tight')
        plt.show() 
    #

    
    
def main():
        
    PD_NC=pathlib.Path(args.NCdir)
    PD_out  =pathlib.Path(args.DIRout)
    tag=args.Tagname
    print(PD_NC, file = sys.stdout)
    print(PD_out, file = sys.stdout)
    print(tag, file = sys.stdout)
    print(NC_file, file = sys.stdout)
    print(L_tracer, file = sys.stdout)
    multi_stackCarbon(PD_NC,tag,PD_out)
    
    
#
if __name__ == "__main__":
    #Initialize
    parser=argparse.ArgumentParser(description="Utilize aggregated/ 1 year and do anal")
     
    #Adding optional parameters
    parser.add_argument('-NCD',
                         '--NCdir',
                         help="NC dir with mode data",
                         required=True,
                         type=str)
    
    parser.add_argument('-T',
                         '--Tagname',
                         help="tag for output file",
                         required=True,
                         type=str)
    
    parser.add_argument('-D)',
                        '--DIRout',
                        help="Output Dir",
                        required=True,
                        type=str)
 
    args = parser.parse_args()
    main()