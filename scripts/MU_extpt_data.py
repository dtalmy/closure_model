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
import cftime
#dir_save='E:\\GCM\\mort_anal\\Darwin_processing'
#dir_location='E:\\GCM\\mort_anal\\Darwin_processing\\T41_data\\mm_10_10_5389956apollo_acf\\*.nc'

# tag=str('test')
# PD_out=pathlib.Path('E:\\Projects\\OceanRelationship\\Histogram\\run_NP2Z1D_long_72237\\NC_trace')
# PF_NC=pathlib.Path('E:\\Projects\\OceanRelationship\\Histogram\\run_NP2Z1D_long_72237\\NC_trace\\GRPD_yr.nc')
# PF_pts=pathlib.Path('E:/Projects/OceanRelationship/Samples/Ir_amt.csv')
#PF_pts=pathlib.Path('E:/Projects/OceanRelationship/Samples/Ext_VB_Data.csv')
def main():
    print(args.LOCfile, file = sys.stdout)
    
    PF_NC=pathlib.Path(args.NCfile)
    PD_out  =pathlib.Path(args.PathFileOut)
    PF_pts=pathlib.Path(args.LOCfile)
    tag=args.Tagname
    #
    ds_tracers=xr.open_mfdataset(PF_NC.as_posix())
    # Identify areas that are not modeled over. (land and seafloor)
    ds_tracers['max_small']= ds_tracers.small_phyto.max(dim={'T'} )
    ds_tracers['Model_area']=xr.where(ds_tracers['max_small'] < 0.0000001,False,True)
    #
    # open csv of pts
    Ext_loc = pd.read_csv(PF_pts.as_posix())
    gdf_loc=    pd.DataFrame (Ext_loc, columns = Ext_loc.columns )
    #
    # for nearest calculation we need longitudes to be positive
    #
    
    def lons_positive(row):
      if row['Longitude'] == -9999 :
          return row['Longitude']
      if row['Longitude'] < 0 :
          return row['Longitude']+360
      return row['Longitude']
    #
    if not 'Longitude_pos' in gdf_loc.columns:
        gdf_loc['Longitude_pos']=gdf_loc.apply (lambda row: lons_positive(row), axis=1)
    #
    # find "nearest"/appropriate index to points (lat,lon,dep,time)
    print('Begin  :: find index', flush=True)
    print('Begin  :: Deps', flush=True, file = sys.stdout)
    gdf_loc['DEPS_index']=ds_tracers.Z.sel(Z=gdf_loc.Depth,method="bfill")
    print('Begin  :: Lats', flush=True, file = sys.stdout)
    gdf_loc['LATS_index']=ds_tracers.sel(X=gdf_loc.Longitude_pos, Y=gdf_loc.Latitude,method="nearest" ).Y
    print('Begin  :: Lons', flush=True, file = sys.stdout)
    gdf_loc['LONS_index']=ds_tracers.sel(X=gdf_loc.Longitude_pos, Y=gdf_loc.Latitude,method="nearest" ).X
    print('End    :: find index', flush=True, file = sys.stdout)
    # set already limited to a single calendar year
    gdf_loc['TIME_index']=np.nan
    def get_time(row):
      tempdate=ds_tracers.T.min()
      used_day=int(row['Day'])
      used_year=int(tempdate.T.dt.year)
      used_month=int(row['Month'])
      # used_day=int(3)
      # used_month=int(2)
      # used_year=int(2008)
      #target_time = np.datetime64(str("{:04d}".format(used_year)) +'-'+ str("{:02d}".format(used_month)) +'-'+ str("{:02d}".format(used_day)))
      #temp=ds_tracers.sel(T=target_time, method='nearest').T.values
      #temp=ds_tracers.sel(T=(ds_tracers.T.dt.month == row['Month']) ).T.values
      dt=cftime.datetime(used_year, used_month,used_day, calendar='360_day')
      #dt = pd.to_datetime(str("{:04d}".format(used_year)) +'-'+ str("{:02d}".format(used_month)) +'-'+ str("{:02d}".format(used_day)))
      temp=ds_tracers.sel(T=dt, method="nearest" ).T.values
      #temp
      return temp
    gdf_loc['TIME_index']=gdf_loc.apply (lambda row: get_time(row), axis=1)
    #
    #
    gdf_loc['M_chk']=False
    gdf_loc['M_DOC']=np.nan
    gdf_loc['M_POC']=np.nan
    gdf_loc['M_DIC']=np.nan
    gdf_loc['M_DOP']=np.nan
    gdf_loc['M_DOFe']=np.nan
    gdf_loc['M_zoo']=np.nan
    gdf_loc['M_virus']=np.nan
    gdf_loc['M_AD']=np.nan
    gdf_loc['M_AP']=np.nan
    gdf_loc['M_large_phyto']=np.nan
    gdf_loc['M_small_phyto']=np.nan
    #
    # Extract
    ds_tracers.load() 
    for i, row in   gdf_loc.iterrows():
        print(i, end =", ", flush=True, file = sys.stdout)
        temp=ds_tracers.loc[dict(Z=gdf_loc.loc[i,'DEPS_index'], Y= gdf_loc.loc[i,'LATS_index'], X= gdf_loc.loc[i,'LONS_index'], T=gdf_loc.loc[i,'TIME_index']) ]
        
        temp2=ds_tracers.loc[dict(Z=gdf_loc.loc[i,'DEPS_index'], Y= gdf_loc.loc[i,'LATS_index'], X= gdf_loc.loc[i,'LONS_index'], T=gdf_loc.loc[i,'TIME_index']) ].values
        temp=ds_tracers.sel(Z=gdf_loc.loc[i,'DEPS_index'], Y= gdf_loc.loc[i,'LATS_index'], X= gdf_loc.loc[i,'LONS_index'], T=gdf_loc.loc[i,'TIME_index'])
        gdf_loc.loc[i,'M_chk']=temp.Model_area.values
        if(gdf_loc.loc[i,'M_chk']==True):
            gdf_loc.loc[i,'M_DOC']=temp.DOC.values
            gdf_loc.loc[i,'M_POC']=temp.POC.values
            gdf_loc.loc[i,'M_DIC']=temp.DIC.values
            gdf_loc.loc[i,'M_DOP']=temp.DOP.values
            gdf_loc.loc[i,'M_DOFe']=temp.DOFe.values
            gdf_loc.loc[i,'M_zoo']=temp.zoo.values
            gdf_loc.loc[i,'M_virus']=temp.virus.values
            gdf_loc.loc[i,'M_AD']=temp.AD.values
            gdf_loc.loc[i,'M_AP']=temp.AP.values
            gdf_loc.loc[i,'M_large_phyto']=temp.large_phyto.values
            gdf_loc.loc[i,'M_small_phyto']=temp.small_phyto.values
    #
    # output
    file_out=PD_out.joinpath(tag+'_ptex.csv')
    print('Write extraction to : '+file_out.as_posix(), file = sys.stdout)
    gdf_loc.to_csv(file_out)
    print('End : EXIT ', file = sys.stdout) 
        
#
if __name__ == "__main__":
    #Initialize
    parser=argparse.ArgumentParser(description="Extract 1 year and aggregate NC files ,write resutls")
     
    #Adding optional parameters
    parser.add_argument('-NC',
                         '--NCfile',
                         help="NC file with model data",
                         required=True,
                         type=str)
    parser.add_argument('-L',
                         '--LOCfile',
                         help="Loc csv file with point data and date. expects certain col.",
                         required=True,
                         type=str)
    parser.add_argument('-T',
                         '--Tagname',
                         help="tag prefix for output file",
                         required=True,
                         type=str)
    parser.add_argument('-PFO',
                        '--PathFileOut',
                        help="path and file name for output csv",
                        required=True,
                        type=str)
 
    args = parser.parse_args()
    main()