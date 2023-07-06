Original 41 tracer model
mod to run4x4

mod to add mortality factors

qsub ./SCR_4x4_t41mort.sh -N t41_1p00_1p00 -v VAR_Xmort=1.0,VAR_X2mort=1.0;

qsub ./SCR_4x4_t41mort.sh -N t41_1p00_0p00 -v VAR_Xmort=1.0,VAR_X2mort=0.0;
qsub ./SCR_4x4_t41mort.sh -N t41_0p00_1p00 -v VAR_Xmort=0.0,VAR_X2mort=1.0;

qsub ./SCR_4x4_t41mort.sh -N t41_0p50_1p00 -v VAR_Xmort=0.5,VAR_X2mort=1.0;
qsub ./SCR_4x4_t41mort.sh -N t41_1p00_0p50 -v VAR_Xmort=1.0,VAR_X2mort=0.5;

qsub ./SCR_4x4_t41mort.sh -N t41_1p50_1p50 -v VAR_Xmort=1.5,VAR_X2mort=1.5;