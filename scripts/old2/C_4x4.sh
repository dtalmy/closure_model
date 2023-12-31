#!/bin/bash

#module load netcdf/4.4.1.1
#module load  gcc/6.3.0
#module load  hdf5/1.10.1
#module load  lapack/3.7.0
alias python=/usr/bin/python2
/lustre/isaac/proj/UTK0105/Darwin/gudb/verification/bacvir_multi/ver_t41mort/scripts
VALpath=/lustre/isaac/proj/UTK0105/Darwin/gudb/verification/bacvir_multi
RUN_ID=test
#VAR_Xmort=1
#VAR_X2mort=1

VALpath=/lustre/isaac/proj/UTK0105/Darwin/gudb/verification/bacvir_multi
USERpath=/lustre/isaac/proj/UTK0105/Darwin/gudb/verification/bacvir_multi
#RUN_ID=$PBS_JOBID
TAG_ID=NP2Z1D
RUN_dir=$VALpath/run_$TAG_ID\_$RUN_ID
RESULTS_DIR=mm_res
GUDBpath=/lustre/isaac/proj/UTK0105/Darwin/gudb
#
#Setup run 
echo RUN_ID    : $RUN_ID
echo TAG_ID    : $TAG_ID
echo VALpath   : $VALpath
echo USERpath  : $USERpath
echo RUN_dir   : $RUN_dir
cd $USERpath
rm -rf ./run_$TAG_ID\_$RUN_ID
mkdir  ./run_$TAG_ID\_$RUN_ID
#lfs setstripe ./run_$TAG_ID\_$RUN_ID -S 32m -i -1 -c 1
cd $VALpath 
ln -s $USERpath/run_$TAG_ID\_$RUN_ID ./run_$TAG_ID\_$RUN_ID
cd   $RUN_dir
#build

cp -r $VALpath/ver_$TAG_ID/* .
# chg mortality modifier
cd ./code

#echo VAR_Xmort    : $VAR_Xmort
#echo VAR_X2mort   : $VAR_X2mort
echo Results dir  : $RESULTS_DIR

#sed -i "s|<VALUE_X_MOD>|$VAR_Xmort|" gud_grazing.F
#sed -i "s|<VALUE_X2_MOD>|$VAR_X2mort|" gud_grazing.F
# print out changed lines for log
#sed '391,400!d' ./gud_grazing.F

cd ..
#
mkdir ./build
cd ./build

if 
  $GUDBpath/tools/genmake2 \
      -rootdir $GUDBpath \
      -mods ../code \
      -mpi  \
      -optfile $GUDBpath/tools/build_options/linux_amd64_ifort+impi_stampede2_skx_isaac
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
#if
#    /usr/bin/time --output=outtime_$RUN_ID.log -p sh -c 'mpirun -np 16 ./mitgcmuv 2>&1 | tee output.log'
#then
#    echo "RUN  succeeded"
#else
#    echo "RUN  failed"
#    exit 1
#fi

#Submit Output processing
#qsub ./scripts/NC_$TAG_ID.sh  -v Pass_DIR=$RUN_DIR,Pass_ID=$RUN_ID,Pass_RN=$RESULTS_DIR

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
