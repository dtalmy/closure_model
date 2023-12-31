#!/bin/bash
#PBS -S /bin/bash
#PBS -A ACF-UTK0105
#PBS -N 4x4_$TAG_ID 
#PBS -m abe
#PBS -M ecarr@utk.edu
#PBS -o /lustre/haven/proj/UTK0105/Darwin/gudb/verification/bacvir_multi/job_data/$PBS_JOBID-out.txt
#PBS -e /lustre/haven/proj/UTK0105/Darwin/gudb/verification/bacvir_multi/job_data/$PBS_JOBID-err.txt
#PBS -l nodes=1:ppn=16
#PBS -l partition=general
#PBS -l feature=skylake
#PBS -l qos=condo
#PBS -l walltime=48:00:00
#PBS - VAR_Xmort 1
#PBS - VAR_X2mort 1
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

VALpath=/lustre/haven/proj/UTK0105/Darwin/gudb/verification/bacvir_multi
USERpath=/lustre/haven/user/werdna/runs
RUN_ID=$PBS_JOBID
TAG_ID=t41mort
DIR_NAME=run_$TAG_ID\_$RUN_ID
USER_DIR=$USERpath/$DIR_NAME
RUN_DIR=$VALpath/$DIR_NAME
RESULTS_DIR=mm_$VAR_Xmort\_$VAR_X2mort\_$RUN_ID
GUDBpath=/lustre/haven/proj/UTK0105/Darwin/gudb
#
#Setup run 
echo RUN_ID    : $RUN_ID
echo TAG_ID    : $TAG_ID
echo VALpath   : $VALpath
echo USERpath  : $USERpath
echo RUN_DIR   : $RUN_DIR
echo USER_DIR   : $USER_DIR
cd $USERpath
if [ -d "$USER_DIR" ]; then
    # Will enter here if $DIRECTORY exists, even if it contains spaces
    echo "User run dir exists  failed"
    exit 1
fi

mkdir  $USER_DIR
lfs setstripe $USER_DIR -S 32m -i -1 -c 1
cd $VALpath 
if [ -d "$RUN_DIR" ]; then
    # Will enter here if $DIRECTORY exists, even if it contains spaces
    echo "RUN area ln dir exists  failed"
    exit 1
fi
cd $VALpath 
ln -s $USER_DIR ./$DIR_NAME
cd   $RUN_DIR
#ln -s $USER_DIR $RUN_DIR

#build

cp -r $VALpath/ver_$TAG_ID/* $RUN_DIR
# chg mortality modifier
# relative links to wokr you must be in the runarea symbolic link
cd   $RUN_DIR
pwd
cd ./code
echo VAR_Xmort    : $VAR_Xmort
echo VAR_X2mort   : $VAR_X2mort
echo Resukts dir  : $RESULTS_DIR

sed -i "s|<VALUE_X_MOD>|$VAR_Xmort|" gud_grazing.F
sed -i "s|<VALUE_X2_MOD>|$VAR_X2mort|" gud_grazing.F
# print out changed lines for log
sed '391,400!d' ./gud_grazing.F

cd $RUN_DIR
#
mkdir ./build
cd ./build

if 
   $GUDBpath/tools/genmake2 \
      -rootdir $GUDBpath \
      -mods ../code \
      -mpi  \
      -optfile $GUDBpath/tools/build_options/linux_amd64_ifort+impi_stampede2_skx_eac
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
cd $RUN_DIR
pwd
if
    /usr/bin/time --output=outtime_$RUN_ID.log -p sh -c 'mpirun -np 16 ./mitgcmuv 2>&1 | tee output.log'
    
then
    echo "RUN  succeeded"
else
    echo "RUN  failed"
    exit 1
fi

#Submit Output processing
qsub ./scripts/NC_$TAG_ID.sh  -N NC$PBS_JOBID -v Pass_DIR=$RUN_DIR,Pass_ID=$RUN_ID,Pass_RN=$RESULTS_DIR

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        