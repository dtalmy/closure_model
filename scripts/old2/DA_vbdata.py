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
from matplotlib.font_manager import FontProperties
#dir_save='E:\\GCM\\mort_anal\\Darwin_processing'
#dir_location='E:\\GCM\\mort_anal\\Darwin_processing\\T41_data\\mm_10_10_5389956apollo_acf\\*.nc'

#tag=str('t41_10_10')
cruise=L_cruise[index_cruise]
PD_out=pathlib.Path('E:/Projects/OceanRelationship/Model_Process/ouput')
#PF_NC=pathlib.Path('E:/Projects/OceanRelationship/Model_Process/GRPD_yr.nc')
PF_data=pathlib.Path('E:/Projects/OceanRelationship/Model_Process/ouput/PD_t41_10_10_20220415-172709.csv')
def graph_vb_cruise(df_data,cruise,title,file_title,legend_pos):
    group=df_data['cruise'].unique()
    print(group)
    cdict = {
        'ARCTICSBI' : 'b',
        'STRATIPHYT1': 'g',
        'USC MO': 'r',
        'STRATIPHYT2': 'c',
        'POWOW': 'm',
        'CASES03-04': 'y',
        'ELA': 'b',
        'TROUT': 'g',
        'SOG' : 'r',
        'SWAT' : 'c',
        'GREENLAND2012' : 'm',
        'NASB2005': 'y',
        'KH05_2' : 'k',
        'KH04_5': 'b',
        'FECYCLE2': 'g',
        'GEOTRACES_LEG3': 'r',
        'GEOTRACES' : 'c',
        'BEDFORDBASIN': 'm',
        'BATS' : 'y',
        'TABASCO': 'k',
        'MOVE': 'b',
        'INDIANOCEAN2006': 'g',
        'FECYCLE1' : 'r',
        'NORTHSEA2001' : 'c',
        'RAUNEFJORD2000': 'm'
    }
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    font.set_style('italic')
    
    #fig = plt.figure(figsize=[18, 9])
    fig,axs =  plt.subplots(1, 2,figsize=[18, 9]) 
    axs[0].set_xlabel('log(bacteria) Microbes per mL log10', fontproperties=font, fontsize='20', fontweight='bold')
    axs[0].set_ylabel('log(virus) Viruses per mL log10', fontproperties=font, fontsize='20', fontweight='bold')
    axs[1].set_xlabel('log(bacteria) (mmol C\\m^3)', fontproperties=font, fontsize='20', fontweight='bold')
    axs[1].set_ylabel('log(virus) (mmol C\\m^3)', fontproperties=font, fontsize='20', fontweight='bold')
    #
    fig.suptitle(str(cruise), fontsize='30')
   # axs[0].set_title("Wigginton Data", fontproperties=font, fontsize='25', fontweight='bold')
   # axs[1].set_title("Darwin", fontproperties=font, fontsize='25', fontweight='bold')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #
    # select cruise data
    #for g in np.unique(group):
    
    df_tmp=df_data.loc[df_data['cruise'] == cruise]
    #axs[0].loglog(df_tmp['virus'],df_tmp['bacteria'],marker=".",linestyle="None",label= 'cruise',c='b')
    xlog=np.log10(df_tmp['bacteria'])
    ylog=np.log10(df_tmp['virus'])
    coef = np.polyfit(xlog,ylog,1)
    poly1d_fn = np.poly1d(coef) 
    axs[0].plot(xlog,ylog,'yo', xlog, poly1d_fn(xlog), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker
    axs[0].axis('equal')
    poly_txt='WD : slope: '+str("%.3f" % coef[0])+'  intercept: '+str("%.3f" % coef[1])
    axs[0].set_title(poly_txt, fontproperties=font, fontsize='20', fontweight='bold')
    #axs[0].text(0.1,0.9,poly_txt,horizontalalignment='center', verticalalignment='center', fontsize='15', transform = axs[0].transAxes)
    
    #axs[1].loglog(df_tmp['M_virus'],df_tmp['M_bactot'],marker=".",linestyle="None",label= 'model',c='r')
    xlog=np.log10(df_tmp['M_bactot'])
    ylog=np.log10(df_tmp['M_virus'])
    coef = np.polyfit(xlog,ylog,1)
    poly1d_fn = np.poly1d(coef) 
    axs[1].plot(xlog,ylog,'ro', xlog, poly1d_fn(xlog), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker
    axs[1].axis('equal')
    poly_txt='Darwin : slope: '+str("%.3f" % coef[0])+'  intercept: '+str("%.3f" % coef[1])
    axs[1].set_title(poly_txt, fontproperties=font, fontsize='20', fontweight='bold')
    #axs[1].text(0.8,0.9,poly_txt,horizontalalignment='center', verticalalignment='center', fontsize='15', transform = axs[0].transAxes)
    
    #
        
    
    
    # print(ax1.get_xlim(), ax1.get_ylim())
    # #lim_value=float(0.00001)
    # #ax1.set(xlim=(lim_value, 10), ylim=(lim_value, 10))
    # ax1.set(xlim=(0.000001, 10), ylim=(0.000001, 10))
    # print(ax1.get_xlim(), ax1.get_ylim())
    # ax1.grid()
    # print(ax1.get_xlim(), ax1.get_ylim())
    # #   
    # #ax1.legend(loc="lower right", title="datasets",fontsize=15, title_fontsize=30, markerscale=3)
    # ax1.legend(loc=legend_pos, title="cruise",fontsize=20, title_fontsize=30, markerscale=3)
    # #
    # #
    # ax1.plot(ax1.get_xlim(), ax1.get_ylim(), ls="--", c=".3")
    #
    fig.tight_layout()
    fig.savefig(file_title,dpi=200, bbox_inches='tight')
    plt.show()
    
def main():
    ##print(args.Datafile, file = sys.stdout)
    ##PF_data=pathlib.Path(args.Datafile)
    ##PD_out  =pathlib.Path(args.DIRout)
    # open csv 
    Ext_data = pd.read_csv(PF_data.as_posix())
    # hatton phyto/zoo dat is in n (mg C/m3)
    # darwin model data: mmol C/m^3
    # 12.07 grams per mole carbon
    df_data=pd.DataFrame (Ext_data, columns = Ext_data.columns )
    df_data=df_data.loc[df_data['M_chk'] == 1]
    L_cruise=df_data.cruise.unique()
    df_data['M_bactot']=df_data['M_AD']+df_data['M_AP']
    #
    index_cruise=2
    filename=str(L_cruise[index_cruise]+'.png')
    file_out=PD_out.joinpath(filename)
    graph_vb_cruise(df_data,L_cruise[index_cruise],str(L_cruise[index_cruise]),file_out,str("upper left"))
    L_cruise
    np.where(L_cruise == 'ARCTICSBI')
    # L_cruise=np.delete(L_cruise,np.where(L_cruise == 'ARCTICSBI'))
    # L_cruise=np.delete(L_cruise,np.where(L_cruise == 'CASES03-04'))
    # L_cruise=np.delete(L_cruise,np.where(L_cruise == 'ELA'))
    # L_cruise=np.delete(L_cruise,np.where(L_cruise == 'TROUT'))
    # L_cruise=np.delete(L_cruise,np.where(L_cruise == 'SOG'))
    for name_cruise in L_cruise:
        print(name_cruise)
        filename=str(name_cruise)+'.png'
        file_out=PD_out.joinpath(filename)
        graph_vb_cruise(df_data,name_cruise,str(name_cruise),file_out,str("upper left"))
#
if __name__ == "__main__":
    #Initialize
    parser=argparse.ArgumentParser(description="Extract 1 year and aggregate NC files ,write resutls")
     
    #Adding optional parameters
    parser.add_argument('-DF',
                         '--Datafile',
                         help="NC file with mode data",
                         required=True,
                         type=str)
    
    parser.add_argument('-D',
                        '--DIRout',
                        help="Output Dir",
                        required=True,
                        type=str)
 
    args = parser.parse_args()
    main()