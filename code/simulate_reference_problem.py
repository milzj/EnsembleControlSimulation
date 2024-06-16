import sys, os

import ensemblecontrol
from harmonic_oscillator import HarmonicOscillator
from harmonic_oscillator.reference_sampler import ReferenceSampler
from plot_state_control import plot_state_control
from stats import save_dict

now = sys.argv[1]
name = sys.argv[2]

outdir = "output/"+now+"/"+name+"/reference_problem/"
os.makedirs(outdir, exist_ok=True)

nsamples = 2**12

harmonic_oscillator = HarmonicOscillator()
sampler = ReferenceSampler()
nparams = harmonic_oscillator.nparams

harmonic_oscillator = HarmonicOscillator()
samples = sampler.sample(nsamples, nparams)
saa_harmonic_oscillator = ensemblecontrol.SAAProblem(harmonic_oscillator, samples)
w_opt, f_opt = saa_harmonic_oscillator.solve()

plot_state_control(harmonic_oscillator, w_opt, nsamples=nsamples, outdir=outdir, filename="reference")

filename = "solutions"
filename = name + "_" + filename + "_{}".format(now)
save_dict(outdir, filename, w_opt)

filename = "optimal_values"
filename = name + "_" + filename + "_{}".format(now)
save_dict(outdir, filename, f_opt)
