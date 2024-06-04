import sys

from casadi import *
from saa_problem import saa_problem
from harmonic_oscillator import HarmonicOscillator
from harmonic_oscillator.sampler import Sampler
from plot_state_control import plot_state_control
from stats import save_dict

now = sys.argv[1]
name = sys.argv[2]

outdir = "output/"+now+"/"+name+"/nominal_problem/"
os.makedirs(outdir, exist_ok=True)

problem = HarmonicOscillator()
w_opt, f_opt = saa_problem(problem, problem.nominal_param)

plot_state_control(problem, w_opt, nsamples=1, outdir=outdir, filename="nominal")
