#!/usr/bin/bash
# --------------------------------------------------
# Request resources here
# --------------------------------------------------
#SBATCH --job-name=job1
#SBATCH --output=job1.out
#SBATCH --account=egornish
#SBATCH --mail-type=END
#SBATCH --mail-user=maria.touceda.suarez@gmail.com
#SBATCH --partition=windfall
#SBATCH --ntasks=16
#SBATCH --nodes=1
#SBATCH --mem=1gb
#SBATCH --time=24:00:00

# --------------------------------------------------
# Load modules here
# --------------------------------------------------

# --------------------------------------------------
# Execute commands here
# --------------------------------------------------

