#!/bin/bash 
#SBATCH -J 4x4_t41
#SBATCH -A ACF-UTK0105
#SBATCH --nodes=1
#SBATCH --cpus-per-task=18
#SBATCH --time=48:00:00
#SBATCH --output=/nfs/home/ecarr/logfiles/NGt41.%j.out
#SBATCH --error=/nfs/home/ecarr/logfiles/NGt41.%j.err
#SBATCH --qos=condo
#SBATCH --partition=condo-dtalmy
##########################################
#                                        #
#   Output some useful job information.  #
#                                        #
##########################################

echo ---Modules 

#setup dir info

#RUN_DIR=/lustre/haven/user/werdna/runs/run_zoomort_5179214.apollo-acf
RUN_DIR=$Pass_DIR
#RUN_ID=zoomort_5179214_v2
RUN_ID=$Pass_ID
RESpath=/$Pass_RN
echo Result processing 

echo RUN_DIR   : $RUN_DIR
echo RUN_ID    : $RUN_ID
echo RESpath   : $RESpath
echo Res Dir   : $RUN_DIR$RESpath

#setup Output processing
cd $RUN_DIR
mkdir $RUN_DIR$RESpath
cd $RUN_DIR$RESpath
#mkdir ./figures

#convert files
cd $RUN_DIR
gluemncbig -o grid.nc  $RUN_DIR/ecco_gud*/grid*.nc
nccopy -k netCDF-4 -d 2 -s  grid.nc $RUN_DIR$RESpath/grid.v4c.nc
rm grid.nc

declare -a arr=("c01" "c02" "c03" "c04" "c05" "c06" "c07" "c08" "c09" "c10"
                "c11" "c12" "c13" "c14" "c15" "c16" "c17" "c18" "c19" "c20"
                "c21" "c22" "c23" "c24" "c25" "c26" "c27" "c28" "c29" "c30"
                "c31" "c32" "c33" "c34" "c35" "c36" "c37" "c38" "c39" "c40"
                "c41"
                )

for tracer in "${arr[@]}"
do
  echo Begin : $tracer
  SECONDS=0
	sleep 3
  gluemncbig -o ptracers.$tracer.nc -v $tracer $RUN_DIR/ecco_gud*/ptracers.0000000*.nc
  nccopy -k netCDF-4 -d 2 -s  ptracers.$tracer.nc $RUN_DIR$RESpath/ptracers.$tracer.v4c.nc
  rm ptracers.$tracer.nc
  echo END Proc. Minutes  : $(( (SECONDS)/60 ))
done

echo process finished

