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
from pylr2 import regress2
import seaborn as sns

#dir_save='E:\\GCM\\mort_anal\\Darwin_processing'
#dir_location='E:\\GCM\\mort_anal\\Darwin_processing\\T41_data\\mm_10_10_5389956apollo_acf\\*.nc'

# tag=str('test')
# #cruise=L_cruise[index_cruise]
# PD_out=pathlib.Path('E:/Projects/OceanRelationship/Histogram/run_NP2Z1D_long_72237/NC_analysis')
# PF_data=pathlib.Path('E:/Projects/OceanRelationship/Histogram/run_NP2Z1D_long_72237/NC_trace/test_ptex.csv')
# #
def graph_zp_map(df_data,title,file_out):
    #
    # filename=str('test_map.png')
    # file_out=PD_out.joinpath(filename)    
    # title='testMAP'
    # 
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    font.set_style('italic')
    #
    fig,ax = plt.subplots(figsize = (18, 12),dpi=300)
    ax = plt.axes(projection=ccrs.Mollweide())
    ax.set_global()
    ax.stock_img()
    ax.coastlines()
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world.plot(ax = ax)
    ax.set_title(title, fontproperties=font, fontsize='30', fontweight='bold')
    L_cruise=df_data.cruise.unique()
    color_labels=df_data.cruise.unique()
    rgb_values = sns.color_palette("rocket", color_labels.size )
    color_map = dict(zip(color_labels, rgb_values))
    for name_cruise in L_cruise:
        print(name_cruise)
        df_data.plot(ax=ax, marker='o', color=df_data['cruise'].map(color_map), markersize=15,transform=ccrs.Geodetic(),label=str(name_cruise) )
    plt.axis('off')
    ax.legend()
    fig.savefig(file_out,dpi=300, bbox_inches='tight')
    plt.show()
#
def graph_zp_hist(df_data,title,file_out):
    # title=str('testHIST')
    # file_out=PD_out.joinpath('hist_testZPhist.png')
    # print('Write to : '+file_out.as_posix(), file = sys.stdout)
    # df_data['phyto']=df_data['Phytoplankton (mg C/m3)']
    # df_data['zoo']=df_data['Microzooplankton (mg C/m3)']
    #
    #
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    font.set_style('italic')
    #
    data_results=[]
    model_results=[]
    combo_si=[]
    L_cruise=df_data.cruise.unique()
    for name_cruise in L_cruise:
        print(name_cruise)
        df_tmp=df_data.loc[df_data['cruise'] == name_cruise]
        #data
        xlog=np.log10(df_tmp['phyto'])
        ylog=np.log10(df_tmp['zoo'])
        data_results = regress2(xlog, ylog, _method_type_2="reduced major axis")
        #model
        xlog=np.log10(df_tmp['M_phyto'])
        ylog=np.log10(df_tmp['M_zoo'])
        model_results = regress2(xlog, ylog, _method_type_2="reduced major axis")
        #
        combo_si.append([name_cruise,model_results['slope'],model_results['intercept'],data_results['slope'],data_results['intercept'] ])
        #
        #
    df_combo_si=pd.DataFrame(combo_si,columns =['cruise','M_slope', 'M_intercept','OD_slope', 'OD_intercept' ])
    #
    fig, axs = plt.subplots(2, 1, sharey=True, tight_layout=True,figsize=[9,12])
    axs[0].set_title(title, fontproperties=font, fontsize='20', fontweight='bold')
    axs[0].hist(df_combo_si['M_slope'], bins='auto',alpha=0.3,color='r', label='Darwin Model')
    axs[0].hist(df_combo_si['OD_slope'], bins='auto',alpha=0.3,color='b', label='Ocean Data')  
    axs[0].legend(loc='upper right')
    #
    cell_text = []
    cell_color = []
    for row in range(len(df_combo_si)):
        #cell_text.append(df_combo_si.iloc[row])        
        text=[df_combo_si.iloc[row][0],str("%.3f" % df_combo_si.iloc[row][1]),str("%.3f" % df_combo_si.iloc[row][2]),str("%.3f" % df_combo_si.iloc[row][3]),str("%.3f" % df_combo_si.iloc[row][4])]
        color=['w','r','r','b','b']
        cell_text.append(text)
        cell_color.append(color)
    #
    axs[1].axis('off')
    data_table=axs[1].table(cellText=cell_text,cellColours=cell_color, colLabels=df_combo_si.columns, loc='center')
    for k, cell in data_table._cells.items():
        cell.set_edgecolor('black')
        if k[0] == 0 or k[1] < 0:
            cell.set_text_props(weight='bold', color='k')
            cell.set_facecolor('g')
            cell.set_alpha(0.3)
        else:
            #cell.set_facecolor(['green', 'yellow'][k[0] % 2])
            cell.set_alpha(0.3)

    axs[1].axis('off')
    #
    fig.tight_layout()
    plt.tight_layout()
    fig.savefig(file_out,dpi=300, bbox_inches='tight')
    plt.show()
    #
    
        
def graph_zp_cruise(df_data,cruise,title,file_out):
    # hatton phyto/zoo dat is in n (mg C/m3)
    # darwin model data: mmol C/m^3
    # 12.07 grams per mole carbon
    # cruise=str('AMT1')
    # title=str('testZP')
    # file_out=PD_out.joinpath(cruise+'_testZP.png')
    # print('Write to : '+file_out.as_posix(), file = sys.stdout)
    # df_data['phyto']=df_data['Phytoplankton (mg C/m3)']
    # df_data['zoo']=df_data['Microzooplankton (mg C/m3)']
    #
    #
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    font.set_style('italic')
    #
    fig,axs =  plt.subplots(1, 2,figsize=[18, 9]) 
    axs[0].set_xlabel('log(phyto) Phytoplankton per mL log10', fontproperties=font, fontsize='20', fontweight='bold')
    axs[0].set_ylabel('log(zoo) Zooplankton per mL log10', fontproperties=font, fontsize='20', fontweight='bold')
    axs[1].set_xlabel('log(M_phyto) Darwin Phyto (mmol C\\m^3)', fontproperties=font, fontsize='20', fontweight='bold')
    axs[1].set_ylabel('log(M_zoo) Darwin Zoo (mmol C\\m^3)', fontproperties=font, fontsize='20', fontweight='bold')
    #
    fig.suptitle(title, fontsize='30')
    #axs[0].set_title("Field Data", fontproperties=font, fontsize='25', fontweight='bold')
    #axs[1].set_title("Darwin Model", fontproperties=font, fontsize='25', fontweight='bold')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #
    # select cruise data
    #for g in np.unique(group):
    
    df_tmp=df_data.loc[df_data['cruise'] == cruise]
    #axs[0].loglog(df_tmp['virus'],df_tmp['bacteria'],marker=".",linestyle="None",label= 'cruise',c='b')
    xlog=np.log10(df_tmp['phyto'])
    ylog=np.log10(df_tmp['zoo'])
    results = regress2(xlog, ylog, _method_type_2="reduced major axis")
    t2=[results['slope'],    results['intercept']]
    poly1d_fn_t2 = np.poly1d(t2) 
    #
    axs[0].plot(xlog,ylog,'yo', xlog, poly1d_fn_t2(xlog), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker
    axs[0].axis('equal')
    regress_txt='Field Data : Regress2 (type2)\n slope: '+str("%.3f" % t2[0])+'  intercept: '+str("%.3f" % t2[1])
    #poly_txt='WD : slope: '+str("%.3f" % coef[0])+'  intercept: '+str("%.3f" % coef[1])
    axs[0].set_title(regress_txt, fontproperties=font, fontsize='20', fontweight='bold')
    #axs[0].text(0.1,0.9,poly_txt,horizontalalignment='center', verticalalignment='center', fontsize='15', transform = axs[0].transAxes)
    
    #axs[1].loglog(df_tmp['M_virus'],df_tmp['M_bactot'],marker=".",linestyle="None",label= 'model',c='r')
    xlog=np.log10(df_tmp['M_phyto'])
    ylog=np.log10(df_tmp['M_zoo'])
    results = regress2(xlog, ylog, _method_type_2="reduced major axis")
    t2=[results['slope'],    results['intercept']]
    poly1d_fn_t2 = np.poly1d(t2) 
    #coef = np.polyfit(xlog,ylog,1)
    #poly1d_fn = np.poly1d(coef) 
    axs[1].plot(xlog,ylog,'ro', xlog, poly1d_fn_t2(xlog), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker
    axs[1].axis('equal')
    regress_txt='Darwin Model : Regress2 (type2)\n slope: '+str("%.3f" % t2[0])+'  intercept: '+str("%.3f" % t2[1])
    #poly_txt='Darwin : slope: '+str("%.3f" % coef[0])+'  intercept: '+str("%.3f" % coef[1])
    axs[1].set_title(regress_txt, fontproperties=font, fontsize='20', fontweight='bold')
    #axs[1].text(0.8,0.9,poly_txt,horizontalalignment='center', verticalalignment='center', fontsize='15', transform = axs[0].transAxes)
    
    
    fig.tight_layout()
    fig.savefig(file_out,dpi=200, bbox_inches='tight')
    plt.show()
#
#    
def main():
    
    PF_data=pathlib.Path(args.ExtLoc)
    PD_out=pathlib.Path(args.DIRout)
    tag=args.Tagname
    print('PF_data: '+ PF_data.as_posix() , flush=True, file = sys.stdout)
    print('PD_out: '+ PD_out.as_posix() , flush=True, file = sys.stdout)
    print('tag: '+ tag , flush=True, file = sys.stdout)
    # open csv 
    Ext_data = pd.read_csv(PF_data.as_posix())
    # hatton phyto/zoo dat is in n (mg C/m3)
    # darwin model data: mmol C/m^3
    # 12.07 grams per mole carbon
    df_data=pd.DataFrame (Ext_data, columns = Ext_data.columns )
    df_data=df_data.loc[df_data['M_chk'] == 1]
    #
    # I need to standardize cruise name currently Name
    L_cruise=df_data.cruise.unique()
    #
    #df_data['M_bactot']=df_data['M_AD']+df_data['M_AP']
    df_data['M_phyto']=df_data['M_large_phyto']+df_data['M_small_phyto']
    df_data['phyto']=df_data['Phytoplankton (mg C/m3)']
    df_data['zoo']=df_data['Microzooplankton (mg C/m3)']
    #
    #print('CSV pt count  = '+str(df_data.latitude.count()), flush=True, file = sys.stdout)
    pts_raw=df_data.latitude.count()
    df_data=df_data.loc[df_data['M_chk'] == 1]
    pts_fmodel=pts_raw-df_data.latitude.count()
    df_data=df_data.loc[df_data['M_zoo'] >0]
    pts_fzoo=pts_raw-pts_fmodel-df_data.latitude.count()
    df_data=df_data.loc[df_data['M_phyto'] >0]
    pts_fphyto=pts_raw-pts_fzoo-pts_fmodel-df_data.latitude.count()
    print('CSV pt original  = '+str(pts_raw), flush=True, file = sys.stdout)
    print('fail chk model   = '+str(pts_fmodel), flush=True, file = sys.stdout)
    print('fail chk zoo     = '+str(pts_fzoo), flush=True, file = sys.stdout)
    print('fail chk phyto   = '+str(pts_fphyto), flush=True, file = sys.stdout)
    print('CSV processed    = '+str(df_data.latitude.count()), flush=True, file = sys.stdout)
    
    #add geometry
    geometry = [Point(xy) for xy in zip(df_data['longitude'], df_data['latitude'])]
    df_data = gpd.GeoDataFrame(df_data, geometry=geometry,crs="EPSG:4326")
    #
    #
    # index_cruise=2
    # filename=str(L_cruise[index_cruise]+'.png')
    # file_out=PD_out.joinpath(filename)
    # graph_vb_cruise(df_data,L_cruise[index_cruise],str(L_cruise[index_cruise]),file_out,str("upper left"))
    # L_cruise
    # np.where(L_cruise == 'ARCTICSBI')
    # L_cruise=np.delete(L_cruise,np.where(L_cruise == 'ARCTICSBI'))
    # L_cruise=np.delete(L_cruise,np.where(L_cruise == 'CASES03-04'))
    # L_cruise=np.delete(L_cruise,np.where(L_cruise == 'ELA'))
    # L_cruise=np.delete(L_cruise,np.where(L_cruise == 'TROUT'))
    # L_cruise=np.delete(L_cruise,np.where(L_cruise == 'SOG'))
    #
    # Generate a map of cruise pts
    #
    map_title=str('Cruise/Model Sampling Location')
    map_out=PD_out.joinpath(tag+'_ZP_mapcombo.png')
    graph_zp_map(df_data,map_title,map_out)
    #
    # Generate the Histogram and table of all the slopes
    #
    hist_title=str('Cruise ZP slope Histogram')
    hist_out=PD_out.joinpath(tag+'_ZP_histcombo.png')
    graph_zp_hist(df_data,hist_title,hist_out)
    #
    # Generate the ind plots for cruises
    #
    for name_cruise in L_cruise:
        print(name_cruise)
        filename=tag+'_ZP_slope_'+str(name_cruise)+'.png'
        cruise_out=PD_out.joinpath(filename)
        title=str('Cruise : '+ name_cruise)
        graph_zp_cruise(df_data,name_cruise,title,cruise_out)
        
#
if __name__ == "__main__":
    #Initialize
    parser=argparse.ArgumentParser(description="Extract 1 year and aggregate NC files ,write resutls")
     
    #Adding optional parameters
    parser.add_argument('-EL',
                         '--ExtLoc',
                         help="CSV file with appened model data",
                         required=True,
                         type=str)
    
    parser.add_argument('-T',
                         '--Tagname',
                         help="tag prefix for output file",
                         required=True,
                         type=str)
    parser.add_argument('-D)',
                        '--DIRout',
                        help="Output Dir",
                        required=True,
                        type=str)
 
    args = parser.parse_args()
    main()