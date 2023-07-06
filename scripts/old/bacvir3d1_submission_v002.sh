#!/bin/bash
#PBS -S /bin/bash
#PBS -A ACF-UTK0105
#PBS -N bacvir3d1_run 
#PBS -m abe
#PBS -M ecarr@utk.edu
#PBS -o /lustre/haven/proj/UTK0105/Darwin/job_data/$PBS_JOBID-out.txt
#PBS -e /lustre/haven/proj/UTK0105/Darwin/job_data/$PBS_JOBID-err.txt
#PBS -l nodes=2:ppn=32
#PBS -l partition=general
#PBS -l feature=skylake
#PBS -l qos=condo
#PBS -l walltime=23:00:00

##########################################
#                                        #
#   Output some useful job information.  #
#                                        #
##########################################
echo ------------------------------------------------------
echo -n 'Job is running on node '; cat $PBS_NODEFILE
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
echo ---Modules 
module load netcdf/4.4.1.1
module load  gcc/6.3.0
module load  hdf5/1.10.1
module load  lapack/3.7.0

VALpath=/lustre/haven/proj/UTK0105/Darwin/gudb/verification/bacvir3d1_eac
echo PBS_JOBID : $PBS_JOBID
echo VALpath   : $VALpath

#
#Setup run 
echo PBS_JOBID : $PBS_JOBID
echo VALpath   : $VALpath
cd $VALpath
mkdir ./run_$PBS_JOBID
cd ./run_$PBS_JOBID
#build

cp -r ../code ./code


mkdir ./build
cd ./build

if 
  ../../../../tools/genmake2 \
      -mods ../code \
      -mpi  \
      -optfile ../../../../tools/build_options/linux_amd64_ifort+impi_stampede2_skx_eac
then
    echo "genmake2 succeeded"
else
    echo "genmake2 failed"
    exit 1
fi

if 
  make depend
then
    echo "make depend succeeded"
else
    echo "make depend failed"
    exit 1
fi

if 
  make 
then
    echo "make  succeeded"
else
    echo "make  failed"
    exit 1
fi
#

cd ..
cp ../input/* .
cp ./build/mitgcmuv .
rm -rf ./build  &
#

#run model
mpirun -np 64 ./mitgcmuv
