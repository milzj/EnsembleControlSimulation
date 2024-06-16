import sys, os

import ensemblecontrol
from harmonic_oscillator import HarmonicOscillator
from harmonic_oscillator.sampler import Sampler
from plot_state_control import plot_state_control
from stats import save_dict

now = sys.argv[1]
name = sys.argv[2]

outdir = "output/"+now+"/"+name+"/saa_problem/"
os.makedirs(outdir, exist_ok=True)


nsamples_vec = [2**k for k in range(1, 9)]
nreplications = 20

harmonic_oscillator = HarmonicOscillator()
sampler = Sampler(nreplications=nreplications)
nparams = harmonic_oscillator.nparams

solution_stats = {}
optimal_value_stats = {}

for nsamples in nsamples_vec:

    sol_stat = {}
    val_stat = {}

    for replication in range(nreplications):

        harmonic_oscillator = HarmonicOscillator()
        samples = sampler.sample(replication, nsamples, nparams)
        saa_harmonic_oscillator = ensemblecontrol.SAAProblem(harmonic_oscillator, samples)
        w_opt, f_opt = saa_harmonic_oscillator.solve()

        sol_stat[replication] = w_opt
        val_stat[replication] = f_opt

        plot_state_control(harmonic_oscillator, w_opt, nsamples=nsamples, outdir=outdir, filename="sample_size={}_replication={}".format(nsamples,replication))

    solution_stats[nsamples] = sol_stat
    optimal_value_stats[nsamples] = val_stat



filename = "solutions"
filename = name + "_" + filename + "_{}".format(now)
save_dict(outdir, filename, solution_stats)

filename = "optimal_values"
filename = name + "_" + filename + "_{}".format(now)
save_dict(outdir, filename, optimal_value_stats)
