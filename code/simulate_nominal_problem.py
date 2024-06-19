import sys, os

import ensemblecontrol
from harmonic_oscillator import HarmonicOscillator
from harmonic_oscillator.sampler import Sampler
from plot_state_control import plot_state_control
from stats import save_dict

now = sys.argv[1]
name = sys.argv[2]

outdir = "output/"+now+"/"+name+"/nominal_problem/"
os.makedirs(outdir, exist_ok=True)

harmonic_oscillator = HarmonicOscillator()
print(harmonic_oscillator.nominal_param)
saa_harmonic_oscillator = ensemblecontrol.SAAProblem(harmonic_oscillator, harmonic_oscillator.nominal_param)
w_opt, f_opt = saa_harmonic_oscillator.solve()

plot_state_control(harmonic_oscillator, w_opt, nsamples=1, outdir=outdir, filename="nominal")
