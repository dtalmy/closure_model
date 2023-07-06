# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 15:15:28 2022

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
#dir_save='E:\\GCM\\mort_anal\\Darwin_processing'
#dir_location='E:\\GCM\\mort_anal\\Darwin_processing\\T41_data\\mm_10_10_5389956apollo_acf\\*.nc'

#tag=str('t41_10_10')

#PD_out=pathlib.Path('E:/Projects/OceanRelationship/Model_Process/ouput')
#PF_NC=pathlib.Path('E:/Projects/OceanRelationship/Model_Process/GRPD_yr.nc')
#PF_data=pathlib.Path('E:/Projects/OceanRelationship/Model_Process/ouput/PD_EXTZP_20220420-122740.csv')
font = FontProperties()
font.set_family('serif')
font.set_name('Times New Roman')
font.set_style('italic')
font.set_size('x-large')
def zp_map(PF_data,PD_out):
    Ext_data = pd.read_csv(PF_data.as_posix())
    # hatton phyto/zoo dat is in n (mg C/m3)
    # darwin model data: mmol C/m^3
    # 12.07 grams per mole carbon
    df_data=pd.DataFrame (Ext_data, columns = Ext_data.columns )
    print('CSV pt count  = '+str(df_data.Latitude.count()), flush=True, file = sys.stdout)
    pts_raw=df_data.Latitude.count()
    df_data=df_data.loc[df_data['M_chk'] == 1]
    pts_fmodel=pts_raw-df_data.Latitude.count()
    df_data=df_data.loc[df_data['zoo'] >0]
    pts_fzoo=pts_raw-pts_fmodel-df_data.Latitude.count()
    df_data=df_data.loc[df_data['phyto'] >0]
    pts_fphyto=pts_raw-pts_fzoo-pts_fmodel-df_data.Latitude.count()
    print('CSV pt original  = '+str(pts_raw), flush=True, file = sys.stdout)
    print('fail chk model   = '+str(pts_fmodel), flush=True, file = sys.stdout)
    print('fail chk zoo     = '+str(pts_fzoo), flush=True, file = sys.stdout)
    print('fail chk phyto   = '+str(pts_fphyto), flush=True, file = sys.stdout)
    print('CSV processed    = '+str(df_data.Latitude.count()), flush=True, file = sys.stdout)
    df_data['M_bactot']=df_data['M_AD']+df_data['M_AP']
    df_data['M_phyto']=df_data['M_large_phyto']+df_data['M_small_phyto']
    #add geometry
    geometry = [Point(xy) for xy in zip(df_data['Longitude'], df_data['Latitude'])]
    df_data = gpd.GeoDataFrame(df_data, geometry=geometry,crs="EPSG:4326")
    #
    #df_data = df_data.to_crs(epsg=4326)
    #
    filename=str('DZP_map.png')
    file_out=PD_out.joinpath(filename)
    #
        
    fig,ax = plt.subplots(figsize = (18, 12),dpi=300)
    ax = plt.axes(projection=ccrs.Mollweide())
    ax.set_global()
    ax.stock_img()
    ax.coastlines()
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world.plot(ax = ax)
    ax.set_title("Zoo/phyto point locations", fontproperties=font, fontsize='30', fontweight='bold')
    df_data.plot(ax=ax, marker='o', color='red', markersize=15,transform=ccrs.Geodetic() )
    plt.axis('off')
    fig.savefig(file_out,dpi=200, bbox_inches='tight')
    plt.show()
    
    
    
def zp_slope(PF_data,PD_out):
    # open csv 
    Ext_data = pd.read_csv(PF_data.as_posix())
    # hatton phyto/zoo dat is in n (mg C/m3)
    # darwin model data: mmol C/m^3
    # 12.07 grams per mole carbon
    df_data=pd.DataFrame (Ext_data, columns = Ext_data.columns )
    print('CSV pt count  = '+str(df_data.Latitude.count()), flush=True, file = sys.stdout)
    pts_raw=df_data.Latitude.count()
    df_data=df_data.loc[df_data['M_chk'] == 1]
    pts_fmodel=pts_raw-df_data.Latitude.count()
    df_data=df_data.loc[df_data['zoo'] >0]
    pts_fzoo=pts_raw-pts_fmodel-df_data.Latitude.count()
    df_data=df_data.loc[df_data['phyto'] >0]
    pts_fphyto=pts_raw-pts_fzoo-pts_fmodel-df_data.Latitude.count()
    print('CSV pt original  = '+str(pts_raw), flush=True, file = sys.stdout)
    print('fail chk model   = '+str(pts_fmodel), flush=True, file = sys.stdout)
    print('fail chk zoo     = '+str(pts_fzoo), flush=True, file = sys.stdout)
    print('fail chk phyto   = '+str(pts_fphyto), flush=True, file = sys.stdout)
    print('CSV processed    = '+str(df_data.Latitude.count()), flush=True, file = sys.stdout)
    df_data['M_bactot']=df_data['M_AD']+df_data['M_AP']
    df_data['M_phyto']=df_data['M_large_phyto']+df_data['M_small_phyto']
    #
    filename=str('DZP_slope.png')
    file_out=PD_out.joinpath(filename)
    #
    #fig,axs =  plt.subplots(2, 2,figsize=[18, 9]) 
    #fig,axs = plt.subplots(nrows=2, ncols=2, figsize=(18, 12))
    fig = plt.figure(tight_layout=True, figsize=(18, 12))
    gs = gridspec.GridSpec(2,2,height_ratios=(6, 2))
    axsA = fig.add_subplot(gs[0, 0])
    axsAt = fig.add_subplot(gs[1, 0])
    axsAt.axis("off")
    axsB = fig.add_subplot(gs[0, 1])
    axsBt = fig.add_subplot(gs[1, 1])
    axsBt.axis("off")
   
    axsA.set_xlabel('log(phyto) ', fontproperties=font,  fontweight='bold')
    axsA.set_ylabel('log(zoo) ', fontproperties=font, fontweight='bold')
    axsB.set_xlabel('log(phyto) (mmol C\\m^3)', fontproperties=font,  fontweight='bold')
    axsB.set_ylabel('log(zoo) (mmol C\\m^3)', fontproperties=font,  fontweight='bold')
    #
    fig.suptitle('zoo/phyto', fontsize='20')
   # axs[0].set_title("Wigginton Data", fontproperties=font, fontsize='25', fontweight='bold')
   # axs[1].set_title("Darwin", fontproperties=font, fontsize='25', fontweight='bold')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #
    # select cruise data
    #for g in np.unique(group):
    
    df_tmp=df_data
    #axs[0].loglog(df_tmp['virus'],df_tmp['bacteria'],marker=".",linestyle="None",label= 'cruise',c='b')
    xlog=np.log10(df_tmp['phyto'])
    ylog=np.log10(df_tmp['zoo'])
    coef = np.polyfit(xlog,ylog,1)
    results = regress2(xlog, ylog, _method_type_2="reduced major axis")
    t2=[results['slope'],    results['intercept']]
    t2
    coef
    poly1d_fn = np.poly1d(coef) 
    poly1d_fnt2 = np.poly1d(t2) 
    
    axsA.plot(xlog,ylog,'yo', label='Collected Values')
    axsA.plot(xlog, poly1d_fn(xlog), '--k',label='type1 fit') #'--k'=black dashed line, 'yo' = yellow circle marker
    axsA.plot( xlog, poly1d_fnt2(xlog), '--r',label='type2 fit')
    axsA.axis('equal')
    #poly_txt='PZbio : slope: '+str("%.3f" % coef[0])+'  intercept: '+str("%.3f" % coef[1])
    data_txt='PZbio\n'
    poly_txt=   'Poly1d   (type1)\n slope: '+str("%.3f" % coef[0])+'  intercept: '+str("%.3f" % coef[1])+'\n'
    regress_txt='Regress2 (type2)\n slope: '+str("%.3f" % t2[0])+'  intercept: '+str("%.3f" % t2[1])
    axsAt.text(0.1, 0.1,data_txt+poly_txt+regress_txt,  verticalalignment='top',horizontalalignment="left",fontsize=25, weight=1000, va='center')
    axsA.set_title(data_txt, fontproperties=font,  fontweight='bold')
    #axs[0].text(0.1,0.9,poly_txt,horizontalalignment='center', verticalalignment='center', fontsize='15', transform = axs[0].transAxes)
    
    #axs[1].loglog(df_tmp['M_virus'],df_tmp['M_bactot'],marker=".",linestyle="None",label= 'model',c='r')
    xlog=np.log10(df_tmp['M_phyto'])
    ylog=np.log10(df_tmp['M_zoo'])
    coef = np.polyfit(xlog,ylog,1)
    poly1d_fn = np.poly1d(coef) 
    results = regress2(xlog, ylog, _method_type_2="reduced major axis")
    t2=[results['slope'],    results['intercept']]
    t2
    coef
    poly1d_fnt2 = np.poly1d(t2) 
    axsB.plot(xlog,ylog,'yo', label='Model Values')
    axsB.plot(xlog, poly1d_fn(xlog), '--k',label='type1 fit') #'--k'=black dashed line, 'yo' = yellow circle marker
    axsB.plot( xlog, poly1d_fnt2(xlog), '--r',label='type2 fit')
    axsB.axis('equal')
    data_txt='Darwin\n'
    poly_txt=   'Poly1d   (type1)\n slope: '+str("%.3f" % coef[0])+'  intercept: '+str("%.3f" % coef[1])+'\n'
    regress_txt='Regress2 (type2)\n slope: '+str("%.3f" % t2[0])+'  intercept: '+str("%.3f" % t2[1])
    axsBt.text(0.1, 0.1,data_txt+poly_txt+regress_txt, verticalalignment='top',horizontalalignment="left",fontsize=25, weight=1000, va='center')
    axsB.set_title(data_txt, fontproperties=font,  fontweight='bold')
    #axs[1].text(0.8,0.9,poly_txt,horizontalalignment='center', verticalalignment='center', fontsize='15', transform = axs[0].transAxes)
    axsA.legend()
    axsB.legend()
    fig.tight_layout()
    fig.savefig(file_out,dpi=200, bbox_inches='tight')
    plt.show()
def main():
    print(args.Datafile, file = sys.stdout)
    PF_data=pathlib.Path(args.CSVpts)
    PD_out  =pathlib.Path(args.DIRout) 
    zp_slope(PF_data,PD_out)
    zp_map(PF_data,PD_out)
#
if __name__ == "__main__":
    #Initialize
    parser=argparse.ArgumentParser(description="Utilize Extracted 1 year and make ZP anal")
     
    #Adding optional parameters
    parser.add_argument('-P',
                         '--CSVpts',
                         help="file of extraction pts",
                         required=True,
                         type=str)
    
    
    parser.add_argument('-D)',
                        '--DIRout',
                        help="Output Dir",
                        required=True,
                        type=str)
 
    args = parser.parse_args()
    main()