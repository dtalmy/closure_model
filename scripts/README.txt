sbatch --job-name=p2z1D5q ./SCR_8x8.sbatch

sbatch --job-name=NC_npzd --export=RUN_DIR=/lustre/isaac/scratch/ecarr/runs/run_NP2Z1D_55680  ./NC_createTracer.sbatch
