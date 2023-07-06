# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 12:15:45 2022

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

#ext_deps_all=[-5.0000e+00, -1.5000e+01, -2.7500e+01, -4.5000e+01, -6.5000e+01, -8.7500e+01, -1.1750e+02, -1.6000e+02]
month_list=[1,2,3,4,5,6,7,8,9,10,11,12]
# L_tracer=[\
#     'c01', \
#     'c02', \
#     'c03'
#     ]
# PD_NC=pathlib.Path('E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1D_long_59771\\NC_trace')
# # #PD_NC=pathlib.Path('E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1Dmay5\\NC_trace')
# PD_out=pathlib.Path('E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1D_long_59771\\NC_analysis')
# tag='59771_'
def initialize(): 
    global ext_deps_all
    ext_deps_all=[-5.0000e+00, -1.5000e+01, -2.7500e+01, -4.5000e+01, -6.5000e+01, -8.7500e+01, -1.1750e+02, -1.6000e+02]
    global month_list
    month_list=[1,2,3,4,5,6,7,8,9,10,11,12]
    #
    global NC_file
    NC_file=[\
        'ptracers.c01.v4c.nc', \
        'ptracers.c02.v4c.nc', \
        'ptracers.c03.v4c.nc', \
        'grid.v4c.nc'          \
        ]
    global L_tracer
    L_tracer=[\
        'c01', \
        'c02', \
        'c03'  \
        ]
    global L_tracer_name
    L_tracer_name=[\
        'L_Phyto', \
        'S_Phyto', \
        'LS_Zoo'  \
        ]
        
def main():
        
    PD_NC=pathlib.Path(args.NCdir)
    PD_out  =pathlib.Path(args.DIRout)
    tag=args.Tagname
    # CL_tracer=args.LISTtrace
    # CL_tracer= CL_tracer.replace('[', ' ').replace(']', ' ').replace(',', ' ').split()
    # print(CL_tracer, file = sys.stdout)
    # L_tracerfile=[]
    # tr_pre=str('ptracers.')
    # tr_post=str('.v4c.nc')
    # for code in CL_tracer:
    #     L_tracerfile.append( tr_pre+str(code)+tr_post)
        
    # #
    # print(L_tracerfile, file = sys.stdout)
    os.chdir(PD_NC)
    P_wd=pathlib.Path.cwd()
    print('Current working dir set to: ' + P_wd.as_posix(), file = sys.stdout )
    #
    #
    ds_tracers=xr.open_mfdataset(NC_file,  combine='by_coords', parallel=False,chunks={'T':1})
    print('Chunks : ' + str(ds_tracers.chunks), file = sys.stdout )
    #
    #limit depth 
    print('Limit depth  :: start', flush=True, file = sys.stdout)
    # #print(ds_tracers.dims, flush=True, file = sys.stdout)
    #ds_tracers=ds_tracers.loc[dict(Z=ext_deps)]
    ds_tracers=ds_tracers.isel(Z=(ds_tracers.Z > (min(ext_deps_all)-1) ) )
    #
    ds_time=ds_tracers.sum(dim=["X", "Y","Z"])
    print('Compute time  :: start', flush=True, file = sys.stdout)
    #ds_time['T'].values
    ds_time=ds_time.compute()
    #ds_time['T'].values
    #
    print('Create figure  :: start', flush=True, file = sys.stdout)
    fig, ax = plt.subplots()
    color = iter(plt.cm.Paired(np.linspace(0, 1,len(L_tracer) )))
    for trace in L_tracer:
        c = next(color)
        s_trace=str(trace)
        print('Plot Sum trace : ' +s_trace, file = sys.stdout)
        ax.plot(ds_time['T'].values, ds_time[s_trace].values,c=c,label=str(s_trace))
    ax.set_title(' Complete time Trace global sum')
    ax.set_ylabel('Sum of tracer Planktonics C (mmol C/m^3)')
    ax.set_xlabel('Model date')
    ax.legend(loc=(1.04,0))
    fig.tight_layout()
    filename=tag+str('_MT_')+str('trace.png')
    file_out=PD_out.joinpath(filename)
    fig.savefig(file_out,dpi=300, bbox_inches='tight')
    plt.show()  
    
    
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
    
    parser.add_argument('-D',
                        '--DIRout',
                        help="Output Dir",
                        required=True,
                        type=str)
    
    # parser.add_argument('-L',
    #                     '--LISTtrace',
    #                     help="list of traces 3 digit code",
    #                     required=True,
    #                     type=str)
 
    args = parser.parse_args()
    initialize() 
    main()