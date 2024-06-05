import sys

from casadi import *
from saa_problem import saa_problem
from harmonic_oscillator import HarmonicOscillator
from harmonic_oscillator.reference_sampler import ReferenceSampler
from stats import load_dict, save_dict

def simulate_criticality_measures(ref_date, saa_date):

    # reference simulation
    outdir = "output/"+ref_date+"/harmonic_oscillator"
    filename = "reference_problem/harmonic_oscillator_optimal_values_{}".format(ref_date)
    ref_value = load_dict(outdir, filename)

    # SAA simulation
    outdir = "output/"+saa_date+"/harmonic_oscillator"
    filename = "harmonic_oscillator_optimal_values_{}".format(saa_date)
    saa_stats = load_dict(outdir, filename)

    now = sys.argv[1]
    name = sys.argv[2]

    N = 2**12

    problem = HarmonicOscillator()
    sampler = ReferenceSampler()
    nparams = problem.nparams

    criticality_measure_stats = {}

    problem = HarmonicOscillator()
    samples = sampler.sample(N, nparams)
    w_opt, f_opt = saa_problem(problem, samples)

    outdir = "output/"+now+"/"+name+"/reference_problem/"
    os.makedirs(outdir, exist_ok=True)

    filename = "solutions"
    filename = name + "_" + filename + "_{}".format(now)
    save_dict(outdir, filename, w_opt)

    filename = "optimal_values"
    filename = name + "_" + filename + "_{}".format(now)
    save_dict(outdir, filename, f_opt)

if __name__ == "__main__":

    ref_date = sys.argv[1]
    saa_date = sys.argv[2]

    simulate_criticality_measures(ref_date, saa_date)
