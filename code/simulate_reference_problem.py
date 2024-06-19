import sys, os

import ensemblecontrol
from plot_state_control import plot_state_control
from stats import save_dict

def simulate_reference_problem(control_problem, sampler, now, name, nsamples):

    outdir = "output/"+now+"/"+name+"/reference_problem/"
    os.makedirs(outdir, exist_ok=True)

    nparams = control_problem.nparams
    samples = sampler.sample(nsamples, nparams)

    saa_control_problem = ensemblecontrol.SAAProblem(control_problem, samples)
    w_opt, f_opt = saa_control_problem.solve()

    plot_state_control(control_problem, w_opt, nsamples=nsamples, outdir=outdir, filename="reference")

    filename = "solutions"
    filename = name + "_" + filename + "_{}".format(now)
    save_dict(outdir, filename, w_opt)

    filename = "optimal_values"
    filename = name + "_" + filename + "_{}".format(now)
    save_dict(outdir, filename, f_opt)


if __name__ == "__main__":

    from harmonic_oscillator import HarmonicOscillator
    from harmonic_oscillator.reference_sampler import ReferenceSampler as HOReferenceSampler

    from cubic_oscillator import CubicOscillator
    from cubic_oscillator.reference_sampler import ReferenceSampler as COReferenceSampler

    now = sys.argv[1]
    name = sys.argv[2]
    nrefsamples = int(sys.argv[3])

    if name == "harmonic_oscillator":
        control_problem = HarmonicOscillator()
        sampler = HOReferenceSampler()
    elif name == "cubic_oscillator":
        control_problem = CubicOscillator()
        sampler = COReferenceSampler()
    else:
        raise NotImplementedError()


    simulate_reference_problem(control_problem, sampler, now, name, nrefsamples)
