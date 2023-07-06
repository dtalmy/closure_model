#!/bin/bash -x
#SBATCH -J NCproc
#SBATCH -A ACF-UTK0105
#SBATCH --exclude=ilp1119,ilp1120
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --time=48:00:00
#SBATCH --output=/nfs/home/ecarr/logfiles/NCproc.%j.out
#SBATCH --error=/nfs/home/ecarr/logfiles/NCproc.%j.err
#SBATCH --qos=condo
#SBATCH --partition=condo-dtalmy

module load zlib/1.2.11-gcc
#load anaconda
module unload PE-intel
module load anaconda3/
source $ANACONDA3_SH
conda activate ma38

RUN_ID=$SLURM_JOB_ID

#setup dir info
if [ -z "$RUN_DIR" ] 
then
  echo "Please set \$RUN_DIR"
  echo "Input failed"
  exit 1
else
	echo "\$RUN_DIR   : $RUN_DIR"
fi
#RUN_DIR=/lustre/isaac/proj/UTK0105/ProjAnal/T41_mort/Model_runs/run_t41mort_5389956.apollo-acf
RESpath=/NC_trace
RESanal=/NC_analysis
RESscripts=/scripts

echo Result processing 

#echo RUN_DIR   : $RUN_DIR
#echo RESpath   : $RESpath
echo Res Dir   : $RUN_DIR$RESpath
echo Res analysis   : $RUN_DIR$RESanal
echo Res scripts   : $RUN_DIR$RESscripts
#setup Output processing
alias python=python3
cd $RUN_DIR
mkdir $RUN_DIR$RESpath
mkdir $RUN_DIR$RESanal
#
# gud files
process_grid=true
if [ "$process_grid" == true ]; then
    echo Processing Grid
    gluemncbig -o grid.nc  $RUN_DIR/ecco_gud*/grid*.nc
    nccopy -k netCDF-4 -d 2 -s  grid.nc $RUN_DIR$RESpath/grid.v4c.nc
    rm grid.nc
fi
#
# gud files
process_gud=false
if [ "$process_gud" == true ]; then
    echo Processing GUD files
    ModelFilePre=gud
    declare -a gudArray=("TRAC01" "TRAC02" "TRAC03" "TRAC04" "TRAC05" \
                         "TRAC06" "TRAC07" "TRAC08" "TRAC09" "TRAC10" \
                         "TRAC11" "TRAC12" "TRAC13" "TRAC14" "TRAC15" \
                         "TRAC16" "TRAC17" "TRAC18" "TRAC19" "TRAC20" \
                         "TRAC21" "TRAC22" "TRAC23" "TRAC24" "TRAC25" \
                         "TRAC26" "TRAC27" "TRAC28" "TRAC29" "TRAC30" \
                         "TRAC31" "TRAC32" "TRAC33" "TRAC34" "TRAC35" \
                         "TRAC36" "TRAC37" "TRAC38" "TRAC39" "TRAC40" \
                         "TRAC41" "TRAC42" "TRAC43" "TRAC44" "TRAC45" \
                         "TRAC46" "TRAC47" "TRAC48" "TRAC49" "TRAC50" \
                         "TRAC51" "TRAC52" "TRAC53" "TRAC54" "TRAC55" \
                         "TRAC56" "TRAC57" "TRAC58" "TRAC59" "TRAC60" \
                         "PAR01" "PP" "BP")
    
    
    
    
    for Tracer_Name in ${gudArray[@]}; do
        
        echo $Tracer_Name
        gluemncbig -o $RUN_DIR/$ModelFilePre.$Tracer_Name.nc -v $Tracer_Name $RUN_DIR/ecco_gud*/$ModelFilePre.0000000*.nc
        nccopy -k netCDF-4 -d 2 -s  $ModelFilePre.$Tracer_Name.nc $RUN_DIR$RESpath/$ModelFilePre.$Tracer_Name.v4c.nc
        rm $ModelFilePre.$Tracer_Name.nc
        # I put Rename proj usr bin
        python3 $RUN_DIR$RESscripts/MU_renameNCtrace.py -fn $ModelFilePre.$Tracer_Name.v4c.nc -D $RUN_DIR$RESpath
    done
else
	echo "\$process_gud not run : $process_gud"    
fi
#
# ptracers files
process_ptracers=true
if [ "$process_ptracers" == true ]; then
    echo Processing ptracers files
    ModelFilePre=ptracers
    declare -a ptArray=("DIC" "NH4" "NO2" "NO3" "PO4"\
                        "SiO2" "FeT" "DOC" "DON" "DOP"\
                        "DOFe" "POC" "PON" "POP" "POSi"\
                        "POFe" "PIC" "ALK" "O2" "c01"\
                        "c02" "c03" "c04" "c05" "c06"\
                        "c07" "c08" "c09" "c10" "c11"\
                        "c12" "c13" "c14" "c15" "c16"\
                        "c17" "c18" "c19" "c20" "c21"\
                        "c22" "c23" "c24" "c25" "c26"\
                        "c27" "c28" "c29" "c30" "c31"\
                        "c32" "c33" "c34" "c35" "c36"\
                        "c37" "c38" "c39" "c40" "c41")
    for Tracer_Name in ${ptArray[@]}; do
        
        echo $Tracer_Name
        gluemncbig -o $RUN_DIR/$ModelFilePre.$Tracer_Name.nc -v $Tracer_Name $RUN_DIR/ecco_gud*/$ModelFilePre.0000000*.nc
        nccopy -k netCDF-4 -d 2 -s  $ModelFilePre.$Tracer_Name.nc $RUN_DIR$RESpath/$ModelFilePre.$Tracer_Name.v4c.nc
        rm $ModelFilePre.$Tracer_Name.nc
		# add calendar 360day to T for appropriate cftime interpretation
        ncatted -a calendar,T,c,c,'360_day' $ModelFilePre.$Tracer_Name.v4c.nc
        # I put Rename proj usr bin
        python3 $RUN_DIR$RESscripts/MU_renameNCtrace.py -fn $ModelFilePre.$Tracer_Name.v4c.nc -D $RUN_DIR$RESpath
    done
else
	echo "\$process_ptracers not run : $process_ptracers"    
fi
#
#
#
cd $RUN_DIR
echo run DA_pt_p2z1_3yr
python3 $RUN_DIR$RESscripts/DA_pt_p2z1_3yr.py \
	-NCD $RUN_DIR$RESpath \
	-T $RUN_ID \
	-D $RUN_DIR$RESanal
#
echo run DA_plot_trace_sum
python3 $RUN_DIR$RESscripts/DA_plot_trace_sum.py \
	-NCD $RUN_DIR$RESpath \
	-T $RUN_ID \
	-D $RUN_DIR$RESanal
#
echo run MU_aggregateyear
python3 $RUN_DIR$RESscripts/MU_aggregateyear.py \
	-MD $RUN_DIR
##
#echo Ext_VB_Data
#python3 $RUN_DIR$RESscripts/MU_extpt_data.py \
#	-NC $RUN_DIR$RESpath/GRPD_yr.nc  \
#	-L $RUN_DIR/scripts/Ext_VB_Data.csv \
#	-T $RUN_ID \
#	-PFO $RUN_DIR$RESpath/PtVB_$RUN_ID\_Ext_VB_Data.csv 
## 
#echo Gen VB graph DA_vbdata
#python3 $RUN_DIR$RESscripts/DA_vbdata.py \
#	-DF $RUN_DIR$RESpath/PtVB_$RUN_ID\_Ext_VB_Data.csv  \
#	-D $RUN_DIR$RESanal
##
echo Ext_ZP_Data
python3 $RUN_DIR$RESscripts/MU_extpt_data.py \
	-NC $RUN_DIR$RESpath/GRPD_yr.nc  \
	-L $RUN_DIR/scripts/Ext_ZP_Data.csv \
	-T $RUN_ID \
	-PFO $RUN_DIR$RESpath/PtZP_$RUN_ID\_Ext_ZP_Data.csv 
# 
echo Gen ZP graph DA_ZPptdata
python3 $RUN_DIR$RESscripts/DA_ZPptdata.py \
	-DF $RUN_DIR$RESpath/PtZP_$RUN_ID\_Ext_ZP_Data.csv 
	-D $RUN_DIR$RESanal
#
#	
echo process finished