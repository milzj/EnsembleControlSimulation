import sys, os

import ensemblecontrol
from plot_state_control import plot_state_control
from stats import save_dict

def simulate_nominal_problem(ControlProblem, now, name):

    outdir = "output/"+now+"/"+name+"/nominal_problem/"
    os.makedirs(outdir, exist_ok=True)

    control_problem = ControlProblem()

    saa_control_problem = ensemblecontrol.SAAProblem(control_problem, control_problem.nominal_param)
    w_opt, f_opt = saa_control_problem.solve()

    plot_state_control(control_problem, w_opt, nsamples=1, outdir=outdir,
                filename= name + "_nominal" + "_{}".format(now))

    filename = "nominal_control"
    filename = name + "_" + filename + "_{}".format(now)
    save_dict(outdir, filename, w_opt)

    filename = "nominal_optimal_value"
    filename = name + "_" + filename + "_{}".format(now)
    save_dict(outdir, filename, f_opt)

if __name__ == "__main__":

    from harmonic_oscillator import HarmonicOscillator
    from cubic_oscillator import CubicOscillator
    from vaccination_scheduling import VaccinationScheduling

    now = sys.argv[1]
    name = sys.argv[2]

    if name == "harmonic_oscillator":
        ControlProblem = HarmonicOscillator
    elif name == "cubic_oscillator":
        ControlProblem = CubicOscillator
    elif name == "vaccination_scheduling":
        ControlProblem = VaccinationScheduling
    else:
        raise NotImplementedError()

    simulate_nominal_problem(ControlProblem, now, name)
