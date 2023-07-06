# -*- coding: utf-8 -*-
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

# tag=str('test')
# PD_out=pathlib.Path('E:\\Projects\\OceanRelationship\\Histogram\\run_NP2Z1D_long_72237')
# PD_NC =pathlib.Path('E:\\Projects\\OceanRelationship\\Histogram\\run_NP2Z1D_long_72237\\NC_trace')
# #=pathlib.Path('E:\\Projects\\OceanRelationship\\Histogram\\run_NP2Z1D_long_72237\\NC_trace')
# NC_file=[\
#     'ptracers.c01.v4c.nc', \
#     'ptracers.c02.v4c.nc', \
#     'ptracers.c03.v4c.nc', \
#     'ptracers.c04.v4c.nc', \
#     'grid.v4c.nc'          \
#     ]
# L_tracer=[\
#     'c01', \
#     'c02', \
#     'c03',  \
#     'c04'  \
#     ]
# ext_deps_all=[-5.0000e+00, -1.5000e+01, -2.7500e+01, -4.5000e+01, -6.5000e+01, -8.7500e+01, -1.1750e+02, -1.6000e+02]
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
        'ptracers.c03.v4c.nc',\
        'grid.v4c.nc'          \
        ]
    global L_tracer
    L_tracer=[\
        'c01', \
        'c02', \
        'c03'\
        ]
    global L_tracer_name
    L_tracer_name=[\
        'L_Phyto', \
        'S_Phyto', \
        'LS_Zoo'\
        ]
    
def gr_Gslopehist(PD_NC,tag,PD_out):
    #
    #
    sys.getrecursionlimit()
    sys.setrecursionlimit(15000) 
    os.chdir(PD_NC)
    P_wd=pathlib.Path.cwd()
    print('Current working dir set to: ' + P_wd.as_posix(), file = sys.stdout )
    #
    filename=tag+str('_Gslopehist.png')
    file_out=PD_out.joinpath(filename)
    ds_tracers=xr.open_mfdataset(NC_file,  combine='by_coords', parallel=False,chunks={'T':1,'Z':1,'Y':2})
    ds_tracers=ds_tracers.drop_dims(['Yp1', 'Xp1','Zp1','Zu','Zl'])
    ds_tracers=ds_tracers.drop('RC')
    ds_tracers=ds_tracers.drop(['drF','dxF','dyF'])
    ds_tracers=ds_tracers.drop(['Ro_surf','HFacC'])
    print('Chunks : ' + str(ds_tracers.chunks), file = sys.stdout )
    ds_tracers=ds_tracers.chunk({'T':1,'Z':23,'Y':2})
    print('Chunks : ' + str(ds_tracers.chunks), file = sys.stdout )
    #
    # limit time
    #time - use  last year 3 years
    print('Limit year  :: start', flush=True, file = sys.stdout)
    tempdate=ds_tracers.T.max()
    YEAR_index=int(tempdate.T.dt.year)
    ds_tracers=ds_tracers.isel(T=(ds_tracers.T.dt.year >= YEAR_index-2))
    ds_tracers=ds_tracers.where(ds_tracers['Depth'] != 0) 
    ds_tracers['bathy_mask']=ds_tracers['Depth'].where(ds_tracers['Depth'] != 0)
    #ds_tracers=ds_tracers.compute()
    #
    #limit depth 
    print('Limit depth and sum :: start', flush=True, file = sys.stdout)
    # #print(ds_tracers.dims, flush=True, file = sys.stdout)
    #ds_tracers=ds_tracers.loc[dict(Z=ext_deps)]
    ds_tracers=ds_tracers.isel(Z=(ds_tracers.Z > (min(ext_deps_all)-1) ) )
    ds_tracers=ds_tracers.sum(dim=["Z"])
    ds_tracers=ds_tracers.compute()
    #
    # Identify areas that are not modeled over and remove 
    #ds_tracers['bathy_mask']=ds_tracers['Depth'].where(ds_tracers['Depth'] != 0)  
    #Tsum_ds_tracers_c01= ds_tracers[c01].max(dim={'T'} )
    #ds_tracers['bathy_mask']=Tsum_ds_tracers_c01.where(Tsum_ds_tracers_c01 < 0.0000001,True,False)
    
    #ds_tracers['bathy_mask'].plot()
    #ds_tracers['c01'].isel(T=0, Z=0).plot()
    #ds_tracers=ds_tracers.where(ds_tracers['Depth'] != 0) 
    #
    #ds_tracers['indexcnt']=xr.zeros_like(ds_tracers['bathy_mask'])
    #count=0
    # ds_tracers['indexcnt'].get_index("X")
    # ds_tracers['indexcnt'].get_index("Y")
    # ds_tracers['indexcnt'].X.size
    # ds_tracers['indexcnt'].sel(X=ds_tracers['indexcnt'].X[0],Y=ds_tracers['indexcnt'].Y[0]).values=2
    # ds_tracers['indexcnt'].sel(X=ds_tracers['indexcnt'].X[0],Y=ds_tracers['indexcnt'].Y[0]).values
    # ds_tracers['indexcnt'].sel(X=0.5,Y=-79.5).values
    # ds_tracers['indexcnt'].loc[dict(X=0.5, Y=-79.5)] = -9999
    #
    # test for loop
#     for yi in np.arange(0,ds_tracers['indexcnt'].Y.size,1):
#         print(yi)
#         for xi in np.arange(0,ds_tracers['indexcnt'].X.size,1):
#             count=count+1
#             ds_tracers['indexcnt'].loc[dict(X=ds_tracers['indexcnt'].X[xi],Y=ds_tracers['indexcnt'].Y[yi])] = count
# #
#     fig, ax = plt.subplots(nrows=1, ncols=1)
#     ds_tracers['indexcnt'].plot(ax=ax)
#     ax.set_title('test loop index')
#     fig.tight_layout()
    #filename=tag+str('_m_mask.png')
    #file_out=PD_out.joinpath(filename)
    #fig.savefig(file_out,dpi=300, bbox_inches='tight')
    #plt.show()    
#
#
    ds_tracers['phyto']=ds_tracers['c01']+ds_tracers['c02']
    ds_tracers['zoo']=ds_tracers['c03']
    #
    #
    ds_tracers['logphyto']=np.log10(ds_tracers['phyto'])
    #ds_tracers['logphyto'].plot()
    ds_tracers['logzoo']=np.log10(ds_tracers['zoo'])
    ds_tracers['slope'] = xr.full_like(ds_tracers['bathy_mask'], fill_value=np.nan)
    ds_tracers['int'] = xr.full_like(ds_tracers['bathy_mask'], fill_value=np.nan)
    print('Comp after log :: start', flush=True, file = sys.stdout)
    ds_tracers.compute()
   
    #
    #limit loop test
    #ystart=105
    #yend=ystart + 2
    #xstart=320
    #xend=xstart+2
    xstart=0
    ystart=0
    yend=ds_tracers['slope'].Y.size
    xend=ds_tracers['slope'].X.size
    a_slope=[]
    for yi in np.arange(ystart,yend,1):
        print(str(yi)+' '+str(datetime.datetime.now()), file = sys.stdout)
        #print(yi, file = sys.stdout)
        #yxlog=ds_tracers['logphyto'].sel(Y=ds_tracers['slope'].Y[yi])
        #yylog=ds_tracers['logzoo'].sel(Y=ds_tracers['slope'].Y[yi])
        #print(yi, file = sys.stdout)
        for xi in np.arange(xstart,xend,1):
            ds_cell=ds_tracers.sel(X=ds_tracers['slope'].X[xi],Y=ds_tracers['slope'].Y[yi])
            if ds_cell['bathy_mask'].values>0:
                #print(str(yi)+' '+str(xi)+' '+str(datetime.datetime.now()), file = sys.stdout)
                # xlog=yxlog.sel(X=ds_tracers['slope'].X[xi]).values
                # ylog=yylog.sel(X=ds_tracers['slope'].X[xi]).values
                #xlog=ds_tracers['logphyto'].sel(X=ds_tracers['slope'].X[xi],Y=ds_tracers['slope'].Y[yi]).values
                # ylog=ds_tracers['logzoo'].sel(X=ds_tracers['slope'].X[xi],Y=ds_tracers['slope'].Y[yi]).values
                xlog=ds_cell['logphyto'].values
                ylog=ds_cell['logzoo'].values
                
                results = regress2(xlog, ylog, _method_type_2="reduced major axis")
                ds_tracers['slope'].loc[dict(X=ds_tracers['slope'].X[xi],Y=ds_tracers['slope'].Y[yi])] =results['slope']
                ds_tracers['int'].loc[dict(X=ds_tracers['slope'].X[xi],Y=ds_tracers['slope'].Y[yi])] =results['intercept']
                a_slope.append(results['slope'])
            else:   
                ds_tracers['slope'].loc[dict(X=ds_tracers['slope'].X[xi],Y=ds_tracers['slope'].Y[yi])] =np.nan
                ds_tracers['int'].loc[dict(X=ds_tracers['slope'].X[xi],Y=ds_tracers['slope'].Y[yi])] =np.nan
            # print(ds_tracers['logphyto'].X[xi].values, file = sys.stdout)
            # print(ds_tracers['logphyto'].Y[yi].values, file = sys.stdout)
            # print(ds_tracers['slope'].sel(X=ds_tracers['slope'].X[xi],Y=ds_tracers['slope'].Y[yi]).values, file = sys.stdout)
            # print(ds_tracers['int'].sel(X=ds_tracers['slope'].X[xi],Y=ds_tracers['slope'].Y[yi]).values, file = sys.stdout)
            # print(results, file = sys.stdout)
    #
    #
    filename=tag+str('_Gslope.nc')
    file_out=PD_out.joinpath(filename)
    ds_tracers.to_netcdf(file_out)
    #
    #ds_w=ds_tracers['slope'].stack(w=("X", "Y"))
    #ds_wv=ds_w.values
    # 
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    font.set_style('italic')
    #
    #
    #fig,ax = plt.subplots(figsize = (18, 12),dpi=300,projection=ccrs.Mollweide())
    #ax = plt.axes(projection=ccrs.Mollweide())
    fig = plt.figure(figsize=(18, 12),dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mollweide())
    ax.set_global()
    #ax.stock_img()
    ax.coastlines()
    #world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    #world.plot(ax = ax)
    #ds_tracers['slope'].plot(ax=ax,transform=ccrs.Geodetic())
    ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
    ds_tracers['slope'].plot.pcolormesh(ax=ax, transform=ccrs.PlateCarree(), x='X', y='Y', add_colorbar=True,zorder=0)
    ax.set_title('Global Slope Value Map', fontproperties=font, fontsize='30', fontweight='bold')
    #plt.axis('off')
    filename=tag+str('_Gslope_map.png')
    file_out=PD_out.joinpath(filename)
    fig.savefig(file_out,dpi=300, bbox_inches='tight')
    plt.show()
    #
    sarr=ds_tracers['slope'].stack(z=("X", "Y"))
    fig, ax = plt.subplots(nrows=1, ncols=1)
    #ax.hist(a_slope, bins=30)
    ax.hist(sarr.values, bins=30)
    ax.set_title('Global Slope Value Histogram')
    fig.tight_layout()
    filename=tag+str('_Gslope_hist.png')
    file_out=PD_out.joinpath(filename)
    fig.savefig(file_out,dpi=300, bbox_inches='tight')
    plt.show()    
    #
    ds_tracers['logslope']=np.log10(ds_tracers['slope'])
    fig = plt.figure(figsize=(18, 12),dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mollweide())
    ax.set_global()
    #ax.stock_img()
    ax.coastlines()
    #world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    #world.plot(ax = ax)
    #ds_tracers['slope'].plot(ax=ax,transform=ccrs.Geodetic())
    ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
    ds_tracers['logslope'].plot.pcolormesh(ax=ax, transform=ccrs.PlateCarree(), x='X', y='Y', add_colorbar=True,zorder=0)
    ax.set_title('Global log10(Slope Value) Map', fontproperties=font, fontsize='30', fontweight='bold')
    #plt.axis('off')
    filename=tag+str('_Gslope_logmap.png')
    file_out=PD_out.joinpath(filename)
    fig.savefig(file_out,dpi=300, bbox_inches='tight')
    plt.show()
    #
    lsarr=ds_tracers['logslope'].stack(z=("X", "Y"))
    fig, ax = plt.subplots(nrows=1, ncols=1)
    #ax.hist(a_slope, bins=30)
    ax.hist(lsarr.values, bins=30)
    ax.set_title('Global log10(Slope Value) Histogram')
    fig.tight_layout()
    filename=tag+str('_Gslope_loghist.png')
    file_out=PD_out.joinpath(filename)
    fig.savefig(file_out,dpi=300, bbox_inches='tight')
    plt.show()    

def main():
        
    PD_NC=pathlib.Path(args.NCdir)
    PD_out  =pathlib.Path(args.DIRout)
    tag=args.Tagname
    print(PD_NC, file = sys.stdout)
    print(PD_out, file = sys.stdout)
    print(tag, file = sys.stdout)
    #
    gr_Gslopehist(PD_NC,tag,PD_out)
    
    
#
if __name__ == "__main__":
    #Initialize
    parser=argparse.ArgumentParser(description="Generate histogram of slope")
     
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
    initialize() 
    main()