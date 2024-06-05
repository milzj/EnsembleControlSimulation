import sys

from casadi import *
from saa_problem import saa_problem
from harmonic_oscillator import HarmonicOscillator
from harmonic_oscillator.sampler import Sampler
from plot_state_control import plot_state_control
from stats import save_dict

now = sys.argv[1]
name = sys.argv[2]

outdir = "output/"+now+"/"+name+"/"
os.makedirs(outdir, exist_ok=True)


sample_sizes = [2**k for k in range(1, 9)]
nreplications = 20

problem = HarmonicOscillator()
sampler = Sampler(nreplications=nreplications)
nparams = problem.nparams

solution_stats = {}
optimal_value_stats = {}

for N in sample_sizes:

    sol_stat = {}
    val_stat = {}

    for replication in range(nreplications):

        problem = HarmonicOscillator()
        samples = sampler.sample(replication, N, nparams)
        w_opt, f_opt = saa_problem(problem, samples)

        sol_stat[replication] = w_opt
        val_stat[replication] = f_opt

        plot_state_control(problem, w_opt, nsamples=N, outdir=outdir, filename="sample_size={}_replication={}".format(N,replication))

    solution_stats[N] = sol_stat
    optimal_value_stats[N] = val_stat



filename = "solutions"
filename = name + "_" + filename + "_{}".format(now)
save_dict(outdir, filename, solution_stats)

filename = "optimal_values"
filename = name + "_" + filename + "_{}".format(now)
save_dict(outdir, filename, optimal_value_stats)
