#!/bin/bash

module load netcdf/4.4.1.1
module load  gcc/6.3.0
module load  hdf5/1.10.1
module load  lapack/3.7.0

VALpath=/lustre/haven/proj/UTK0105/Darwin/gudb/verification/bacvir_multi
RUN_ID=test

#
#Setup run 
echo RUN_ID    : $RUN_ID
echo VALpath   : $VALpath
cd $VALpath
rm -rf ./run_zoomort_$RUN_ID
mkdir  ./run_zoomort_$RUN_ID
cd     ./run_zoomort_$RUN_ID
#build

cp -r ../ver_zoomort/* .

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
