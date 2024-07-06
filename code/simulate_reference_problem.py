import sys, os

import ensemblecontrol
from plot_state_control import plot_state_control
from stats import save_dict

def simulate_reference_problem(ControlProblem, Sampler, now, name, nsamples, nreplications):

    outdir = "output/"+now+"/"+name+"/reference_problem/"
    os.makedirs(outdir, exist_ok=True)


    for nreplication in range(nreplications):

        control_problem = ControlProblem()
        sampler = Sampler(nreplications)
        nparams = control_problem.nparams
        samples = sampler.sample(nsamples, nparams, nreplication)

        saa_control_problem = ensemblecontrol.SAAProblem(control_problem, samples)
        w_opt, f_opt = saa_control_problem.solve()

        filename = "rep_{}".format(nreplication)
        filename = "reference_" + name + "_" + filename + "_{}".format(now)
        plot_state_control(control_problem, w_opt, nsamples=nsamples,
                            outdir=outdir,
                            filename=filename)

        filename = "solutions_rep_{}".format(nreplication)
        filename = name + "_" + filename + "_{}".format(now)
        save_dict(outdir, filename, w_opt)

        filename = "optimal_values_rep_{}".format(nreplication)
        filename = name + "_" + filename + "_{}".format(now)
        save_dict(outdir, filename, f_opt)


if __name__ == "__main__":

    from harmonic_oscillator import HarmonicOscillator
    from harmonic_oscillator.reference_sampler import ReferenceSampler as HOReferenceSampler

    from cubic_oscillator import CubicOscillator
    from cubic_oscillator.reference_sampler import ReferenceSampler as COReferenceSampler

    from vaccination_scheduling import VaccinationScheduling
    from vaccination_scheduling.reference_sampler import ReferenceSampler as VSReferenceSampler


    now = sys.argv[1]
    name = sys.argv[2]
    nrefsamples = int(sys.argv[3])
    nreplications = int(sys.argv[4])

    if name == "harmonic_oscillator":
        ControlProblem = HarmonicOscillator
        Sampler = HOReferenceSampler
    elif name == "cubic_oscillator":
        ControlProblem = CubicOscillator
        Sampler = COReferenceSampler
    elif name == "vaccination_scheduling":
        ControlProblem = VaccinationScheduling
        Sampler = VSReferenceSampler
    else:
        raise NotImplementedError()


    simulate_reference_problem(ControlProblem, Sampler, now, name, nrefsamples, nreplications)
