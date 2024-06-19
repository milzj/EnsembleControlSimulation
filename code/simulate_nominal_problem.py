import sys, os

import ensemblecontrol
from plot_state_control import plot_state_control
from stats import save_dict

def simulate_nominal_problem(control_problem, now, name):

    outdir = "output/"+now+"/"+name+"/nominal_problem/"
    os.makedirs(outdir, exist_ok=True)

    saa_control_problem = ensemblecontrol.SAAProblem(control_problem, control_problem.nominal_param)
    w_opt, f_opt = saa_control_problem.solve()

    plot_state_control(control_problem, w_opt, nsamples=1, outdir=outdir, filename="nominal")


if __name__ == "__main__":

    from harmonic_oscillator import HarmonicOscillator
    from cubic_oscillator import CubicOscillator

    now = sys.argv[1]
    name = sys.argv[2]

    if name == "harmonic_oscillator":
        control_problem = HarmonicOscillator()
    elif name == "cubic_oscillator":
        control_problem = CubicOscillator()
    else:
        raise NotImplementedError()


    simulate_nominal_problem(control_problem, now, name)
