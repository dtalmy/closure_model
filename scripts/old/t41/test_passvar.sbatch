#!/bin/bash 
#SBATCH -J 4x4_t41
#SBATCH -A ACF-UTK0105
#SBATCH --nodes=1
#SBATCH --cpus-per-task=11
#SBATCH --time=48:00:00
#SBATCH --output=/nfs/home/ecarr/logfiles/test.%j.out
#SBATCH --error=/nfs/home/ecarr/logfiles/test.%j.err
#SBATCH --qos=condo
#SBATCH --partition=condo-dtalmy
##########################################
#                                        #
#   Output some useful job information.  #
#                                        #
##########################################
echo "print variable"
echo $aaa

if [ -z "$aaa" ] 
then
  echo "Please set \$aaa"
  echo "Input failed"
  exit 1
else
	echo "\$aaa  : $aaa"
fi
#
if [ -z "$bbb" ] 
then
  echo "Please set \$bbb"
  echo "Input failed"
  exit 1
else
	echo "\$bbb  : $bbb"
fi
#
if [ -z "$notset" ] 
then
  echo "Please set \$notset"
  echo "Input failed"
  exit 1
else
	echo "\$notset  : $notset"
fi
exit 0