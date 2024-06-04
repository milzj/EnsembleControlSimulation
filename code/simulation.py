import os, sys
import numpy as np
import matplotlib

from casadi import *
from harmonic_oscillator.reference_sampler import ReferenceSampler
from harmonic_oscillator import HarmonicOscillator
from problem.integrator import Integrator
from problem.ensemble_rhs import EnsembleRHS
from problem.optimization_problem import OptimizationProblem
from plot_state_control import plot_state_control

harmonic_oscillator = HarmonicOscillator()
harmonic_oscillator.nintervals = nintervals

nstates = harmonic_oscillator.nstates
alpha = harmonic_oscillator.alpha
nparams = harmonic_oscillator.nparams
final_time = harmonic_oscillator.final_time
ncontrols = harmonic_oscillator.ncontrols

parameterized_initial_value = harmonic_oscillator.parameterized_initial_value
parametric_rhs, control_regularizer, control = harmonic_oscillator.parameterized_rhs
objective_function = harmonic_oscillator.objective_function
lbu = harmonic_oscillator.lbu
ubu = harmonic_oscillator.ubu
mesh_width = harmonic_oscillator.mesh_width

nsamples = 2**3
reference_sampler = ReferenceSampler()
samples = reference_sampler.sample(nsamples, nparams)

nensemblestates = nstates*nsamples

# ensemble right hand side
ensemble_rhs, ensemble_initial_value = EnsembleRHS(parametric_rhs,
                    control_regularizer, control,
                    parameterized_initial_value,
                    samples, nstates, nensemblestates)

integrator = Integrator(ensemble_rhs, final_time, nintervals, nensemblestates, ncontrols)

objective, constraints, decisions, initial_decisions, lbw, ubw, lbg, ubg = \
                            OptimizationProblem(objective_function, integrator, lbu, ubu, 
                            ensemble_initial_value, alpha, nensemblestates, ncontrols, 
                            nsamples, nintervals)

problem = {'f': objective, 'x': decisions, 'g': constraints}
solver = nlpsol('solver', 'ipopt', problem);

# Solve the NLP
sol = solver(x0=initial_decisions, lbx=lbw, ubx=ubw, lbg=lbg, ubg=ubg)
w_opt = sol['x'].full().flatten()


plot_state_control(w_opt, nstates, ncontrols, nsamples, nintervals, mesh_width, alpha)
