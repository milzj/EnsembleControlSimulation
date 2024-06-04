import sys

from casadi import *
from saa_problem import saa_problem
from harmonic_oscillator import HarmonicOscillator
from harmonic_oscillator.reference_sampler import ReferenceSampler
from plot_state_control import plot_state_control
from stats import save_dict


now = sys.argv[1]
name = sys.argv[2]

outdir = "output/"+now+"/"+name+"/reference_problem/"
os.makedirs(outdir, exist_ok=True)

N = 2**12

problem = HarmonicOscillator()
sampler = ReferenceSampler()
nparams = problem.nparams

solution_stats = {}
optimal_value_stats = {}

problem = HarmonicOscillator()
samples = sampler.sample(N, nparams)
w_opt, f_opt = saa_problem(problem, samples)

plot_state_control(problem, w_opt, nsamples=N, outdir=outdir, filename="reference")

filename = "solutions"
filename = name + "_" + filename + "_{}".format(now)
save_dict(outdir, filename, w_opt)

filename = "optimal_values"
filename = name + "_" + filename + "_{}".format(now)
save_dict(outdir, filename, f_opt)
