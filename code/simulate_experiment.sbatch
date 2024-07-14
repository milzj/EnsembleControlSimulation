#!/bin/bash

#SBATCH -J SimExp-Fixed-Control                    # Job name
#SBATCH --account=gts-jmilz3                     # charge account
#SBATCH -N 1 --ntasks-per-node=1                  # number of nodes and cores per node
#SBATCH --mem-per-cpu=16gb                        # Memory per core
#SBATCH -qinferno                               # QOS Name
#SBATCH -o output/Report-%x-%j.out                         # Combined output and error messages file
#SBATCH --mail-type=ALL              # Mail preferences
#SBATCH --mail-user=jmilz3@gatech.edu           # E-mail address for notifications
#SBATCH --time=08:00:00

module load python

cd $HOME/EnsembleControlSimulation
source .venv/bin/activate

export PYTHONPATH=$HOME/EnsembleControlSimulation:${PYTHONPATH}
export PYTHONPATH=$HOME/EnsembleControlSimulation/code:${PYTHONPATH}


cd $HOME/EnsembleControlSimulation/code/
source simulate_problems.sh















