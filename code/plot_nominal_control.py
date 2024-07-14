import sys, os

import ensemblecontrol
from plot_state_control import plot_state_control
from stats import load_dict

if __name__ == "__main__":

    from harmonic_oscillator import HarmonicOscillator

    name = "harmonic_oscillator"
    control_problem = HarmonicOscillator()

    outdir = "output/06-Jul-2024-14-14-20/" + name
    filename = "nominal_problem/harmonic_oscillator_nominal_control_06-Jul-2024-14-14-20"

    w_opt = load_dict(outdir, filename)

    outdir = "output/06-Jul-2024-14-14-20/" + name + "/nominal_problem"
    filename = "harmonic_oscillator_nominal_control_06-Jul-2024-14-14-20"
    plot_state_control(control_problem, w_opt, nsamples=1, outdir=outdir,
                filename=filename, ylim=[-3.294,3.294])

