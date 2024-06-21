import sys, os

import ensemblecontrol
from plot_state_control import plot_state_control
from stats import save_dict

def simulate_saa_problem(ControlProblem, Sampler, now, name, nreplications, lbrange, ubrange):

    nsamples_vec = [2**k for k in range(lbrange, ubrange)]

    outdir = "output/"+now+"/"+name+"/saa_problem/"
    os.makedirs(outdir, exist_ok=True)

    control_problem = ControlProblem()
    sampler = Sampler(nreplications=nreplications)
    nparams = len(control_problem.nominal_param[0])

    solution_stats = {}
    optimal_value_stats = {}

    for nsamples in nsamples_vec:

        sol_stat = {}
        val_stat = {}

        for replication in range(nreplications):

            control_problem = ControlProblem()
            samples = sampler.sample(replication, nsamples, nparams)
            saa_control_problem = ensemblecontrol.SAAProblem(control_problem, samples)
            w_opt, f_opt = saa_control_problem.solve()

            sol_stat[replication] = w_opt
            val_stat[replication] = f_opt

            plot_state_control(control_problem, w_opt, nsamples=nsamples, outdir=outdir, filename="sample_size={}_replication={}".format(nsamples,replication))

        solution_stats[nsamples] = sol_stat
        optimal_value_stats[nsamples] = val_stat


    filename = "solutions"
    filename = name + "_" + filename + "_{}".format(now)
    save_dict(outdir, filename, solution_stats)

    filename = "optimal_values"
    filename = name + "_" + filename + "_{}".format(now)
    save_dict(outdir, filename, optimal_value_stats)


if __name__ == "__main__":

    from harmonic_oscillator import HarmonicOscillator
    from harmonic_oscillator.sampler import Sampler as HOSampler

    from cubic_oscillator import CubicOscillator
    from cubic_oscillator.sampler import Sampler as COSampler

    from vaccination_scheduling import VaccinationScheduling
    from vaccination_scheduling.sampler import Sampler as VSSampler

    now = sys.argv[1]
    name = sys.argv[2]
    nreplications = int(sys.argv[3])
    lbrange = int(sys.argv[4])
    ubrange = int(sys.argv[5])

    if name == "harmonic_oscillator":
        ControlProblem = HarmonicOscillator
        Sampler = HOSampler
    elif name == "cubic_oscillator":
        ControlProblem = CubicOscillator
        Sampler = COSampler
    elif name == "vaccination_scheduling":
        ControlProblem = VaccinationScheduling
        Sampler = VSSampler
    else:
        raise NotImplementedError()


    simulate_saa_problem(ControlProblem, Sampler, now, name, nreplications, lbrange, ubrange)
