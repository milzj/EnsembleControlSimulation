import sys, os
from base import idx_state_control

import ensemblecontrol
from harmonic_oscillator import HarmonicOscillator
from harmonic_oscillator.reference_sampler import ReferenceSampler
from stats import load_dict, save_dict


def simulate_criticality_measures(saa_date, problem_id):

    # SAA simulation
    outdir = "output/"+saa_date+"/{}".format(problem_id)
    filename = "{}_solutions_{}".format(problem_id,saa_date)
    saa_controls = load_dict(outdir, filename)

    nsamples_vec = list(saa_controls.keys())
    nreplications = len(saa_controls[nsamples_vec[0]].keys())

    now = sys.argv[1]
    name = sys.argv[2]

    nrefsamples = 2**12

    harmonic_oscillator = HarmonicOscillator()
    sampler = ReferenceSampler()
    nparams = harmonic_oscillator.nparams

    harmonic_oscillator = HarmonicOscillator()
    samples = sampler.sample(nrefsamples, nparams)
    saa_harmonic_oscillator = ensemblecontrol.SAAProblem(harmonic_oscillator, samples, MultipleShooting=False)

    # compute control bounds
    nintervals = harmonic_oscillator.nintervals
    lbu, ubu = harmonic_oscillator.control_bounds
    lb_vec = nintervals*lbu
    ub_vec = nintervals*ubu
    mesh_width = harmonic_oscillator.mesh_width

    # control idx
    nstates = harmonic_oscillator.nstates
    ncontrols = harmonic_oscillator.ncontrols

    criticality_measure_stats = {}

    for nsamples in nsamples_vec:

        cm_stat = {}
        idx_state, idx_control = idx_state_control(nstates, ncontrols, nsamples, nintervals)
        idx_control = idx_control.flatten()
        idx_control.sort()

        print("nsamples={}\n\n".format(nsamples))

        for replication in range(nreplications):

            w_saa = saa_controls[nsamples][replication]

            u_saa = w_saa[idx_control]

            deriv_saa = saa_harmonic_oscillator.derivative(u_saa)
            grad_saa = deriv_saa/mesh_width
            cm = ensemblecontrol.base.canonical_criticality_measure(u_saa, grad_saa, lb_vec, ub_vec, mesh_width)

            cm_stat[replication] = cm
            print(cm)

        criticality_measure_stats[nsamples] = cm_stat

    outdir = "output/"+now+"/"+name+"/saa_problem/"
    os.makedirs(outdir, exist_ok=True)

    filename = "criticality_measures"
    filename = name + "_" + filename + "_{}".format(now)
    save_dict(outdir, filename, criticality_measure_stats)


if __name__ == "__main__":

    saa_date = sys.argv[1]
    problem_id = sys.argv[2]

    simulate_criticality_measures(saa_date, problem_id)
