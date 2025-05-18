import pickle
import ensemblecontrol
import numpy as np
from base import idx_state_control
from harmonic_oscillator import HarmonicOscillator
from harmonic_oscillator.reference_sampler import ReferenceSampler as HOReferenceSampler
from vaccination_scheduling import VaccinationScheduling
from vaccination_scheduling.reference_sampler import ReferenceSampler as VSReferenceSampler

# Utility to extract control from state-control vector
def extract_control(state_control, nstates, ncontrols, nsamples, nintervals):
    _, idx_control = idx_state_control(nstates, ncontrols, nsamples=nsamples, nintervals=nintervals)
    return state_control[idx_control.flatten(order='F')]

# Paths
ho_nom_path = "output/06-Jul-2024-14-14-20/harmonic_oscillator/nominal_problem/harmonic_oscillator_nominal_control_06-Jul-2024-14-14-20.pickle"
vs_nom_path = "output/06-Jul-2024-14-14-20/vaccination_scheduling/nominal_problem/vaccination_scheduling_nominal_control_06-Jul-2024-14-14-20.pickle"
ho_ref_path = "output/06-Jul-2024-14-14-20/harmonic_oscillator/reference_problem/harmonic_oscillator_solutions_rep_0_06-Jul-2024-14-14-20.pickle"
vs_ref_path = "output/06-Jul-2024-14-14-20/vaccination_scheduling/reference_problem/vaccination_scheduling_solutions_rep_0_06-Jul-2024-14-14-20.pickle"

# Problem setup
nreplications = 1
nrep = 0
nsamples = 2**12

# Harmonic Oscillator
ho_problem = HarmonicOscillator()
ho_sampler = HOReferenceSampler(nreplications)
ho_samples = ho_sampler.sample(nsamples, ho_problem.nparams, nrep)
ho_saa = ensemblecontrol.SAAProblem(ho_problem, ho_samples, MultipleShooting=False)
with open(ho_nom_path, "rb") as f:
    ho_nom_state = pickle.load(f)
with open(ho_ref_path, "rb") as f:
    ho_ref_state = pickle.load(f)
ho_nom_control = extract_control(ho_nom_state, ho_problem.nstates, ho_problem.ncontrols, 1, ho_problem.nintervals)
ho_ref_control = extract_control(ho_ref_state, ho_problem.nstates, ho_problem.ncontrols, 2**12, ho_problem.nintervals)
ho_nom_val = ho_saa(ho_nom_control)
ho_ref_val = ho_saa(ho_ref_control)
print("Harmonic Oscillator SAA objective at nominal control:")
print(ho_nom_val)
print("Harmonic Oscillator SAA objective at reference control:")
print(ho_ref_val)

# Vaccination Scheduling
vs_problem = VaccinationScheduling()
vs_sampler = VSReferenceSampler(nreplications)
vs_samples = vs_sampler.sample(nsamples, vs_problem.nparams, nrep)
vs_saa = ensemblecontrol.SAAProblem(vs_problem, vs_samples, MultipleShooting=False)
with open(vs_nom_path, "rb") as f:
    vs_nom_state = pickle.load(f)
with open(vs_ref_path, "rb") as f:
    vs_ref_state = pickle.load(f)
vs_nom_control = extract_control(vs_nom_state, vs_problem.nstates, vs_problem.ncontrols, 1, vs_problem.nintervals)
vs_ref_control = extract_control(vs_ref_state, vs_problem.nstates, vs_problem.ncontrols, 2**12, vs_problem.nintervals)
vs_nom_val = vs_saa(vs_nom_control)
vs_ref_val = vs_saa(vs_ref_control)
print("\nVaccination Scheduling SAA objective at nominal control:")
print(vs_nom_val)
print("Vaccination Scheduling SAA objective at reference control:")
print(vs_ref_val)

# Save optimal values to text files in the reference_problem folder
with open("output/06-Jul-2024-14-14-20/harmonic_oscillator/reference_problem/value-of-stochastic-solution.txt", "w") as f:
    f.write(f"SAA objective evaluated at nominal_control {ho_nom_val}\n")
    f.write(f"SAA objective evaluated at reference_control {ho_ref_val}\n")
    f.write(f"value of stochastic solution {ho_nom_val-ho_ref_val}\n")
    f.write(f"relative value of stochastic solution {(ho_nom_val-ho_ref_val)/ho_ref_val}\n")

with open("output/06-Jul-2024-14-14-20/vaccination_scheduling/reference_problem/value-of-stochastic-solution.txt", "w") as f:
    f.write(f"SAA objective evaluated at nominal_control {vs_nom_val}\n")
    f.write(f"SAA objective evaluated at reference_control {vs_ref_val}\n")
    f.write(f"value of stochastic solution {vs_nom_val-vs_ref_val}\n")
    f.write(f"relative value of stochastic solution {(vs_nom_val-vs_ref_val)/vs_ref_val}\n")