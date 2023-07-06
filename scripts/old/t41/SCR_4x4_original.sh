#!/bin/bash
#PBS -S /bin/bash
#PBS -A ACF-UTK0105
#PBS -N 4x4_original
#PBS -m abe
#PBS -M ecarr@utk.edu
#PBS -o /lustre/haven/proj/UTK0105/Darwin/gudb/verification/bacvir_multi/job_data/$PBS_JOBID-out.txt
#PBS -e /lustre/haven/proj/UTK0105/Darwin/gudb/verification/bacvir_multi/job_data/$PBS_JOBID-err.txt
#PBS -l nodes=1:ppn=16
#PBS -l partition=general
#PBS -l feature=skylake
#PBS -l qos=condo
#PBS -l walltime=48:00:00

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
#module load  gcc/6.3.0
module load gcc/10.1.0
module load  hdf5/1.10.1
module load  lapack/3.7.0

VALpath=/lustre/haven/proj/UTK0105/Darwin/gudb/verification/bacvir_multi
RUN_ID=$PBS_JOBID

#
#Setup run 
echo RUN_ID    : $RUN_ID
echo VALpath   : $VALpath
cd $VALpath
rm -rf ./run_original_$RUN_ID
mkdir  ./run_original_$RUN_ID
cd     ./run_original_$RUN_ID
#build

cp -r ../ver_original/* .

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
ln -s ./input/* .
cp ./build/mitgcmuv .
#rm -rf ./build  &
#

#run model
#mpirun -np 16 ./mitgcmuv


#run model
if
    /usr/bin/time --output=outtime_$RUN_ID.log -p sh -c 'mpirun -np 16 ./mitgcmuv 2>&1 | tee output.log'
then
    echo "RUN  succeeded"
else
    echo "RUN  failed"
    exit 1
fi


##setup Output processing
#mkdir ./results_$PBS_JOBID
#cd ./results_$PBS_JOBID
#mkdir ./figures
#
#python3 ../scripts/gluemncbig.py -o grid.nc  ecco_gud*/grid*.nc
#nccopy -k netCDF-4 -d 2 -s  grid.nc grid.v4c.nc
#rm grid.nc
#python3 ../scripts/gluemncbig.py -o ptracers.c01.nc -v 'c01' ecco_gud*/ptracers.0000000*.nc
#nccopy -k netCDF-4 -d 2 -s  ptracers.c01.nc ptracers.c01.v4c.nc
#rm ptracers.c01.nc
#python3 ../scripts/gluemncbig.py -o ptracers.c02.nc -v 'c02' ecco_gud*/ptracers.0000000*.nc
#nccopy -k netCDF-4 -d 2 -s  ptracers.c02.nc ptracers.c02.v4c.nc
#rm ptracers.c02.nc
#python3 ../scripts/gluemncbig.py -o ptracers.c03.nc -v 'c03' ecco_gud*/ptracers.0000000*.nc
#nccopy -k netCDF-4 -d 2 -s  ptracers.c03.nc ptracers.c03.v4c.nc
#rm ptracers.c03.nc
#python3 ../scripts/gluemncbig.py -o ptracers.c04.nc -v 'c04' ecco_gud*/ptracers.0000000*.nc
#nccopy -k netCDF-4 -d 2 -s  ptracers.c04.nc ptracers.c04.v4c.nc
#rm ptracers.c04.nc
#python3 ../scripts/gluemncbig.py -o ptracers.c05.nc -v 'c05' ecco_gud*/ptracers.0000000*.nc
#nccopy -k netCDF-4 -d 2 -s  ptracers.c05.nc ptracers.c05.v4c.nc
#rm ptracers.c05.nc
#python3 ../scripts/gluemncbig.py -o ptracers.c06.nc -v 'c06' ecco_gud*/ptracers.0000000*.nc
#nccopy -k netCDF-4 -d 2 -s  ptracers.c06.nc ptracers.c06.v4c.nc
#rm ptracers.c06.nc
