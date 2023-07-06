#!/bin/bash
# script to document building model
module load netcdf/4.4.1.1
module load  gcc/6.3.0
module load  hdf5/1.10.1
echo `module list` 1>&2

RUNNAME='run_test'
mkdir ../$RUNNAME

cd ../build

# remove everythin in build
make CLEAN

if 
  ../../../tools/genmake2 \
      -mods ../code \
      -mpi  \
      -optfile ../../../tools/build_options/linux_amd64_ifort+impi_stampede2_skx_eac
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

cd ../$RUNNAME
ln -s ../input/* .
cp ../build/mitgcmuv .

exit
