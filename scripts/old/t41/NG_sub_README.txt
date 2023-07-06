qsub ./SCR_4x4_t41mort.sh -N t41_0p50_1p00 -v VAR_Xmort=0.5,VAR_X2mort=1.0;
VAR_Xmort=0.9
echo $VAR_Xmort
VAR_X2mort=0.9
echo $VAR_X2mort
sbatch --job-name=t41_1p0_1p0  --export=VAR_Xmort=1.0,VAR_X2mort=1.0 ./SCRng_4x4_t41mort.sbatch


sbatch --job-name=t41_1p0_1p0  --export=VAR_Xmort=1.0,VAR_X2mort=0.0 ./SCRng_4x4_t41mort.sbatch
sbatch --job-name=t41_1p0_1p0  --export=VAR_Xmort=0.0,VAR_X2mort=1.0 ./SCRng_4x4_t41mort.sbatch

sbatch --job-name=NC_proc  --export=RUN_DIR=/lustre/isaac/scratch/ecarr/runs/run_t41mort_24661 ./NG_submission_fixed.sbatch



sbatch --job-name=t_aaa  --export=aaa=1.23,bbb=0.9 ./test_passvar.sbat