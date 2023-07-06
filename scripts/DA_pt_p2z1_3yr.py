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

font = FontProperties()
font.set_family('serif')
font.set_name('Times New Roman')
font.set_style('italic')
font.set_size('x-large')

ext_deps_all=[-5.0000e+00, -1.5000e+01, -2.7500e+01, -4.5000e+01, -6.5000e+01, -8.7500e+01, -1.1750e+02, -1.6000e+02]
month_list=[1,2,3,4,5,6,7,8,9,10,11,12]
#PF_NC=pathlib.Path('E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1D\\NC_trace\\GRPD_yr.nc')
#PD_NC=pathlib.Path('E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1D\\NC_trace\\')
#PD_out  =pathlib.Path('E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1D\\NC_analysis')
#
# PD_NC=pathlib.Path('E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1Dmay5\\NC_trace\\')
# PD_out  =pathlib.Path('E:\\Projects\\OceanRelationship\\Model_Process\\NP2Z1Dmay5\\NC_analysis')
# tag='NPZD'

    
    
# L4
# Latitude:   50.2500     Longitude:   -4.2167    
#lat=50.2500
#long=-4.2167    

def gr_sumline(PF_NC,tag,PD_out):
    #
    filename=str('Dsum_LineSum.png')
    file_out=PD_out.joinpath(filename)
    #
    os.chdir(PD_NC)
    P_wd=pathlib.Path.cwd()
    print('Current working dir set to: ' + P_wd.as_posix(), file = sys.stdout )
    #
    NC_file=NC_fileptracer
    ds_tracers=xr.open_mfdataset(NC_file,  combine='by_coords', parallel=False)
    # Identify areas that are not modeled over. (land and seafloor)
    Tsum_ds_tracers_c01= ds_tracers.c01.max(dim={'T'} )
    ds_tracers['bathy_mask']=Tsum_ds_tracers_c01.where(Tsum_ds_tracers_c01 < 0.0000001,True,False)
    #
    ds_tracers['zoo']=ds_tracers['c03']
    ds_tracers['phyto']=ds_tracers['c01']+ds_tracers['c02']
    #
    #limit depth
    print('Limit depth  :: start', flush=True, file = sys.stdout)
    ds_tracers=ds_tracers.isel(Z=(ds_tracers.Z > (min(ext_deps_all)-1) ) )
    #
    #ds_tracers['bactot']=ds_tracers['AD']+ds_tracers['AP']
    #ds_tracers['vb']=np.log10(ds_tracers['virus'])/np.log10(ds_tracers['bactot'])
    #ds_tracers['phyto']=ds_tracers['large_phyto']+ds_tracers['small_phyto']
    #ds_tracers['zp']=np.log10(ds_tracers['zoo'])/np.log10(ds_tracers['phyto'])
    #line graph
    #ds_tracers
    ds_time=ds_tracers.sum(dim=["X", "Y","Z"])
    ds_max=ds_tracers.max(dim=["X", "Y","Z"])
    ds_mean=ds_tracers.mean(dim=["X", "Y","Z"])
    ds_min=ds_tracers.min(dim=["X", "Y","Z"])
    #vonvert time units
   
    ds_time['periodT']=ds_time['T'].values-ds_time['T'].values.min()
    ps=pd.Series(ds_time['periodT'].values)
    # ps.dt.days
    # ds_time['zoo'].values
    # ds_time['large_phyto'].values
    # plt.plot(ps.dt.days,ds_time['zoo'].values, ds_time['large_phyto'].values)
    # ds_time['periodT'].values
    #
    fig, axs = plt.subplots(2, 1,tight_layout=True, figsize=(9, 12))
    axs[0].plot(ps.dt.days, ds_time['c03'].values,'-b',label='zoo')
    axs[0].plot(ps.dt.days, ds_time['c01'].values,'-g',label='First_phyto')
    axs[0].plot(ps.dt.days, ds_time['c02'].values,'-m',label='Second_phyto')
    #axs[0].set_xlim(0, 2)
    axs[0].set_xlabel('time(days)')
    axs[0].set_ylabel('plankton(mmol C/m^3)')
    axs[0].grid(True)
    axs[0].legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol=3)
    #
    # ax2 = axs[0].twinx()
    # color = 'tab:red'
    # ax2.set_ylabel('mean zp ratio', color=color)  # we already handled the x-label with ax1
    # ax2.plot(ps.dt.days, ds_max['zp'].values, '--k',label='max zp ratio')
    # ax2.plot(ps.dt.days, ds_min['zp'].values, '--k',label='min zp ratio')
    # ax2.plot(ps.dt.days, ds_mean['zp'].values, '--r',label='mean zp ratio')
    # ax2.tick_params(axis='y', labelcolor=color)
    # ax2.legend(bbox_to_anchor=(0,1.12,1,0.2), loc="lower left",
    #         mode="expand", borderaxespad=0, ncol=3)
    # axs[1].set_xlabel('time(days)')
    # axs[1].set_ylabel('Virus/Bact(mmol C/m^3)')
    # axs[1].plot(ps.dt.days, ds_time['virus'].values,label='virus')
    # axs[1].plot(ps.dt.days, ds_time['AP'].values,label='AP')
    # axs[1].plot(ps.dt.days, ds_time['AD'].values,label='AD')
    # axs[1].legend(loc=(1.04,0.5))
    # #
    axs[1].set_xlabel('time(days)')
    axs[1].set_ylabel('abiotic log10(mmol C/m^3)')
    axs[1].grid(True)
    axs[1].plot(ps.dt.days, np.log10(ds_time['DIC'].values),'--b',label='DIC')
    axs[1].plot(ps.dt.days, np.log10(ds_time['DOC'].values),'--r',label='DOC')
    axs[1].plot(ps.dt.days, np.log10(ds_time['DOFe'].values),'--g',label='DOFe')
    axs[1].plot(ps.dt.days, np.log10(ds_time['DOP'].values),'--m',label='DOP')
    axs[1].plot(ps.dt.days, np.log10(ds_time['POC'].values),'--y',label='POC')
    axs[1].legend(loc=(1.04,0))
    fig.tight_layout()
    fig.savefig(file_out,dpi=200, bbox_inches='tight')
    plt.show()
 
def gr_Locationline(lat,long,PD_NC,tag,PD_out):
    #
    filename=str(tag+'_lat_'+str(lat)+'_long_'+str(long)+'.png')
    file_out=PD_out.joinpath(filename)
    #
    os.chdir(PD_NC)
    P_wd=pathlib.Path.cwd()
    print('Current working dir set to: ' + P_wd.as_posix(), file = sys.stdout )
    #
    NC_fileptracer=[\
        'ptracers.c01.v4c.nc' , \
        'ptracers.c02.v4c.nc' , \
        'ptracers.c03.v4c.nc', \
        'ptracers.DIC.v4c.nc' , \
        'ptracers.DOC.v4c.nc' , \
        'ptracers.DOFe.v4c.nc' , \
        'ptracers.DOP.v4c.nc' , \
        'ptracers.POC.v4c.nc' \
        ]
    #    
    NC_file=NC_fileptracer
    ds_tracers=xr.open_mfdataset(NC_file,  combine='by_coords', parallel=False)
    # Identify areas that are not modeled over. (land and seafloor)
    Tsum_ds_tracers_c01= ds_tracers.c01.max(dim={'T'} )
    ds_tracers['bathy_mask']=Tsum_ds_tracers_c01.where(Tsum_ds_tracers_c01 < 0.0000001,True,False)
    #
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
    ds_tracers['zoo']=ds_tracers['c03']
    ds_tracers['phyto']=ds_tracers['c01']+ds_tracers['c02']
    #
    #ds_tracers['bactot']=ds_tracers['AD']+ds_tracers['AP']
    #ds_tracers['vb']=np.log10(ds_tracers['virus'])/np.log10(ds_tracers['bactot'])
    #ds_tracers['phyto']=ds_tracers['large_phyto']+ds_tracers['small_phyto']
    #ds_tracers['zp']=np.log10(ds_tracers['zoo'])/np.log10(ds_tracers['phyto'])
    #line graph
    # ds_tracers
    # ds_time=ds_tracers.sum(dim=["X", "Y","Z"])
    # ds_max=ds_tracers.max(dim=["X", "Y","Z"])
    # ds_mean=ds_tracers.mean(dim=["X", "Y","Z"])
    # ds_min=ds_tracers.min(dim=["X", "Y","Z"])
    #vonvert time units
    #
    # Extract data at point
    
    
    long_pos=long
    if long_pos < 0 :
          long_pos=long_pos+360
    #
    gdf_loc_list=[lat,long,long_pos,0,2000,12,31]
    gdf_loc_colnames=['lats','lons','lons_pos','deps','year','month','day']
    gdf_loc=    pd.DataFrame ([gdf_loc_list], columns = gdf_loc_colnames )
    #Create Geomtry point
    geometry = [Point(xy) for xy in zip(gdf_loc['lons_pos'], gdf_loc['lats'])]
    crs = {'init': 'epsg:4326'}
    gdf_loc = gpd.GeoDataFrame(gdf_loc, crs=crs, geometry=geometry)
    gdf_loc.iloc[0].lats
    gdf_loc['geometry']
    #
    #
    # find "nearest"/appropriate index to points (lat,lon,dep,time)
    print('Begin  :: find index', flush=True)
    print('Begin  :: Deps', flush=True, file = sys.stdout)
    gdf_loc['DEPS_index']=ds_tracers.Z.sel(Z=gdf_loc.deps,method="bfill")
    print('Begin  :: Lats', flush=True, file = sys.stdout)
    gdf_loc['LATS_index']=ds_tracers.sel(X=gdf_loc.lons_pos, Y=gdf_loc.lats,method="nearest" ).Y
    print('Begin  :: Lons', flush=True, file = sys.stdout)
    gdf_loc['LONS_index']=ds_tracers.sel(X=gdf_loc.lons_pos, Y=gdf_loc.lats,method="nearest" ).X
    print('End    :: find index', flush=True, file = sys.stdout)
    #
    i=0
    
    print('Extract Loc :: start :: '+ str(gdf_loc.iloc[0].lats)+" "+str(gdf_loc.iloc[0].lons_pos) , flush=True, file = sys.stdout)
    
    ds_loc=ds_tracers.loc[dict( Y= gdf_loc.loc[i,'LATS_index'], X= gdf_loc.loc[i,'LONS_index']) ]
    ds_loc=ds_loc.sum(dim=["Z"])
    ds_time=ds_loc
    if ds_time['bathy_mask']:
   
       
        ds_time['periodT']=ds_time['T'].values-ds_time['T'].values.min()
        ps=pd.Series(ds_time['periodT'].values)
        # ps.dt.days
        # ds_time['zoo'].values
        # ds_time['large_phyto'].values
        # plt.plot(ps.dt.days,ds_time['zoo'].values, ds_time['large_phyto'].values)
        # ds_time['periodT'].values
        #
        fig = plt.figure(figsize=[18, 18])
        ax0 = fig.add_subplot(2, 2, 2)
        ax1 = fig.add_subplot(2, 2, 4, sharex=ax0)
        ax2 = fig.add_subplot(2, 2, 3, projection=ccrs.Mollweide())
        ax3 = fig.add_subplot(2, 2, 1)
        #
        ax0.plot(ps.dt.days, ds_time['c03'].values,'-b',label='zoo')
        ax0.plot(ps.dt.days, ds_time['c01'].values,'-g',label='phyto c01')
        ax0.plot(ps.dt.days, ds_time['c02'].values,'--m',label='phyto c02')
        #ax0.set_xlim(0, 2)
        ax0.set_xlabel('time(days)')
        ax0.set_ylabel('plankton(mmol C/m^3)')
        ax0.grid(True)
        ax0.legend(loc=(1.04,0))
        #ax0.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",mode="expand", borderaxespad=0, ncol=3)
        #
        # ax2 = axs[0].twinx()
        # color = 'tab:red'
        # ax2.set_ylabel('mean zp ratio', color=color)  # we already handled the x-label with ax1
        # ax2.plot(ps.dt.days, ds_max['zp'].values, '--k',label='max zp ratio')
        # ax2.plot(ps.dt.days, ds_min['zp'].values, '--k',label='min zp ratio')
        # ax2.plot(ps.dt.days, ds_mean['zp'].values, '--r',label='mean zp ratio')
        # ax2.tick_params(axis='y', labelcolor=color)
        # ax2.legend(bbox_to_anchor=(0,1.12,1,0.2), loc="lower left",
        #         mode="expand", borderaxespad=0, ncol=3)
        # ax1.set_xlabel('time(days)')
        # ax1.set_ylabel('Virus/Bact(mmol C/m^3)')
        # ax1.plot(ps.dt.days, ds_time['virus'].values,label='virus')
        # ax1.plot(ps.dt.days, ds_time['AP'].values,label='AP')
        # ax1.plot(ps.dt.days, ds_time['AD'].values,label='AD')
        # ax1.legend(loc=(1.04,0.5))
        # #
        ax1.set_xlabel('time(days)')
        ax1.set_ylabel('abiotic log10(mmol C/m^3)')
        ax1.grid(True)
        ax1.plot(ps.dt.days, np.log10(ds_time['DIC'].values),'--b',label='DIC')
        ax1.plot(ps.dt.days, np.log10(ds_time['DOC'].values),'--r',label='DOC')
        ax1.plot(ps.dt.days, np.log10(ds_time['DOFe'].values),'--g',label='DOFe')
        ax1.plot(ps.dt.days, np.log10(ds_time['DOP'].values),'--m',label='DOP')
        ax1.plot(ps.dt.days, np.log10(ds_time['POC'].values),'--y',label='POC')
        ax1.legend(loc=(1.04,0))
        #
        #ax2.set_global()
        ax2.set_extent([gdf_loc.loc[i,'LONS_index']-40, gdf_loc.loc[i,'LONS_index']+40, gdf_loc.loc[i,'LATS_index']-20, gdf_loc.loc[i,'LATS_index']+20], ccrs.Geodetic())
        ax2.stock_img()
        ax2.coastlines()
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        world.plot(ax = ax2)
        str_title='Ext Loc: '+ str(gdf_loc.iloc[0].lats)+" "+str(gdf_loc.iloc[0].lons_pos) 
        ax2.set_title(str_title, fontproperties=font, fontsize='20', fontweight='bold')
        gdf_loc.plot( marker='o', color='red', markersize=30,transform=ccrs.Geodetic(),ax=ax2 )
        #
        # create zp plot
        xlog=np.log10(ds_time['phyto'])
        ylog=np.log10(ds_time['zoo'])
        ptcolor=ds_time['T'].dt.month.values
        results = regress2(xlog.values, ylog.values, _method_type_2="reduced major axis")
        t2=[results['slope'],    results['intercept']]
        t2
        poly1d_fnt2 = np.poly1d(t2)
        regress_txt='Regress2 (type2)\n slope: '+str("%.3f" % t2[0])+'  intercept: '+str("%.3f" % t2[1])
        ax3.set_title(regress_txt, fontproperties=font,  fontweight='bold')
        ax3.set_xlabel('log(phyto) (mmol C\\m^3)', fontproperties=font,  fontweight='bold')
        ax3.set_ylabel('log(zoo) (mmol C\\m^3)', fontproperties=font,  fontweight='bold')
        #ax3.plot(xlog,ylog,'yo', label='Model Values')
        hdl_scatter=ax3.scatter(xlog,ylog,c=ptcolor, cmap='hsv', label='Model Values')
        hdl_line=ax3.plot( xlog, poly1d_fnt2(xlog), '--r',label='type2 fit')
        ax3.legend(handles=[hdl_line], loc='lower right')
        #ax3.legend(handles=[hdl_scatter], loc='upper left')
        legend1 = ax3.legend(*hdl_scatter.legend_elements(num=12),
                    loc="upper left", title="Month")
        ax3.add_artist(legend1)

        #
        #
        fig.tight_layout()
        fig.savefig(file_out,dpi=200, bbox_inches='tight')
        plt.show()    
    else:
        print('Extract Loc ::OUTSIDE MODEL AREA :: '+ str(gdf_loc.iloc[0].lats)+" "+str(gdf_loc.iloc[0].lons_pos) +" "+str(ds_time['bathy_mask']), flush=True, file = sys.stdout)
    
def main():
        
    PD_NC=pathlib.Path(args.NCDir)
    PD_out  =pathlib.Path(args.DIRout)
    tag=args.Tagname
    print('PD_NC   :: '+pathlib.Path(PD_NC).as_posix(), flush=True, file = sys.stdout)
    print('PD_out  :: '+pathlib.Path(PD_out).as_posix(), flush=True, file = sys.stdout)
    print('tag     :: '+ tag, flush=True, file = sys.stdout)
    # L4
    # Latitude:   50.2500     Longitude:   -4.2167
    # for nearest calculation we need longitudes to be positive
    #
    #shift to get to active model cell
    lat=0
    long=-26    
    gr_Locationline(lat,long,PD_NC,tag,PD_out)
    lat=30.
    long=-26   
    gr_Locationline(lat,long,PD_NC,tag,PD_out)
    lat=60
    long=-26
    gr_Locationline(lat,long,PD_NC,tag,PD_out)
    lat=-30.
    long=-26   
    gr_Locationline(lat,long,PD_NC,tag,PD_out)
    lat=-60.
    long=-26   
    gr_Locationline(lat,long,PD_NC,tag,PD_out)
#
if __name__ == "__main__":
    #Initialize
    parser=argparse.ArgumentParser(description="Ext point anal")
     
    #Adding optional parameters
    parser.add_argument('-NCD',
                         '--NCDir',
                         help="NC Dir with mode data",
                         required=True,
                         type=str)
    
    parser.add_argument('-T',
                         '--Tagname',
                         help="tag for outpur file",
                         required=True,
                         type=str)
    
    parser.add_argument('-D)',
                        '--DIRout',
                        help="Output Dir",
                        required=True,
                        type=str)
 
    args = parser.parse_args()
    main()