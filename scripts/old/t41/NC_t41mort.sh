#!/bin/bash
#PBS -S /bin/bash
#PBS -A ACF-UTK0105
#PBS -N NCsubproc
#PBS -m abe
#PBS -M ecarr@utk.edu
#PBS -o /lustre/haven/proj/UTK0105/Darwin/gudb/verification/bacvir_multi/job_data/$PBS_JOBID-out.txt
#PBS -e /lustre/haven/proj/UTK0105/Darwin/gudb/verification/bacvir_multi/job_data/$PBS_JOBID-err.txt
#PBS -l nodes=1:ppn=4
#PBS -l partition=general
#PBS -l feature=skylake
#PBS -l qos=condo
#PBS -l walltime=12:30:00
#PBS - Pass_DIR test
#PBS - Pass_ID test 
#PBS - Pass_RN test 
##########################################
#                                        #
#   Output some useful job information.  #
#                                        #
##########################################
echo ------------------------------------------------------
echo -n "Job is running on node "; cat $PBS_NODEFILE
echo ------------------------------------------------------
echo PBS: qsub is running on $PBS_O_HOST
echo PBS: originating queue is $PBS_O_QUEUE
echo PBS: executing queue is $PBS_QUEUE
echo PBS: working directory is $PBS_O_WORKDIR
echo PBS: execution mode is $PBS_ENVIRONMENT
echo PBS: job identifier is $PBS_JOBID
echo PBS: job name is $PBS_JOBNAME
echo PBS: node file is $PBS_NODEFILE
echo "$PBS_NODEFILE"
echo $(more $PBS_NODEFILE)
echo PBS: current home directory is $PBS_O_HOME
echo PBS: PATH = $PBS_O_PATH
echo -----------------------------------------------------
echo -----------------------------------------------------

module load netcdf/4.4.1.1
module load  gcc/6.3.0
module load  hdf5/1.10.1
module load  lapack/3.7.0

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

