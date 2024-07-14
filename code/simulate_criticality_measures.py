import sys, os
from base import idx_state_control

import ensemblecontrol
from stats import load_dict, save_dict
import numpy as np

def simulate_criticality_measures(ControlProblem, Sampler, saa_date, name, nrefsamples, nrefreplications):

    # SAA simulation
    outdir = "output/"+saa_date+"/{}/saa_problem".format(name)
    filename = "{}_solutions_{}".format(name,saa_date)
    saa_controls = load_dict(outdir, filename)

    nsamples_vec = list(saa_controls.keys())
    nreplications = len(saa_controls[nsamples_vec[0]].keys())

    control_problem = ControlProblem()

    # compute control bounds
    nintervals = control_problem.nintervals
    lbu, ubu = control_problem.control_bounds
    lb_vec = nintervals*lbu
    ub_vec = nintervals*ubu
    mesh_width = control_problem.mesh_width

    # control idx
    nstates = control_problem.nstates
    ncontrols = control_problem.ncontrols

    criticality_measure_stats = {}

    for nsamples in nsamples_vec:

        print("nsamples={}\n\n".format(nsamples))

        cm_stat = {}
        idx_state, idx_control = idx_state_control(nstates, ncontrols, nsamples, nintervals)
        idx_control = idx_control.flatten()
        idx_control.sort()

        for replication in range(nreplications):

            w_saa = saa_controls[nsamples][replication]
            u_saa = w_saa[idx_control]

            deriv_saa = []
            for nrefreplication in range(nrefreplications):

                sampler = Sampler(nrefreplications)
                nparams = control_problem.nparams
                samples = sampler.sample(nrefsamples, nparams, nrefreplication)
                saa_control_problem = ensemblecontrol.SAAProblem(control_problem, samples, MultipleShooting=False)
                deriv_saa.append( saa_control_problem.derivative(u_saa) )

            deriv_saa = np.mean(deriv_saa, axis=0)

            grad_saa = deriv_saa/mesh_width
            cm = ensemblecontrol.base.canonical_criticality_measure(u_saa, grad_saa, lb_vec, ub_vec, mesh_width)

            cm_stat[replication] = cm

        criticality_measure_stats[nsamples] = cm_stat

    outdir = "output/"+saa_date+"/"+name+"/saa_problem/"
    os.makedirs(outdir, exist_ok=True)

    filename = "criticality_measures"
    filename = name + "_" + filename + "_rep_{}".format(saa_date)
    save_dict(outdir, filename, criticality_measure_stats)

if __name__ == "__main__":

    from harmonic_oscillator import HarmonicOscillator
    from harmonic_oscillator.reference_sampler import ReferenceSampler as HOReferenceSampler

    from cubic_oscillator import CubicOscillator
    from cubic_oscillator.reference_sampler import ReferenceSampler as COReferenceSampler

    from vaccination_scheduling import VaccinationScheduling
    from vaccination_scheduling.reference_sampler import ReferenceSampler as VSReferenceSampler

    saa_date = sys.argv[1]
    name = sys.argv[2]
    nrefsamples = int(sys.argv[3])
    nrefreplications = int(sys.argv[4])

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


    simulate_criticality_measures(ControlProblem, Sampler, saa_date, name, nrefsamples, nrefreplications)
