import os, sys
import numpy as np
import matplotlib

from casadi import *
from problem.rk4_integrator import RK4Integrator
from problem.ensemble_rhs import EnsembleRHS
from problem.multiple_shooting_optimization_problem import MultipleShootingOptimizationProblem

def saa_problem(problem, samples):

    nstates = problem.nstates
    nintervals = problem.nintervals
    alpha = problem.alpha
    nparams = problem.nparams
    final_time = problem.final_time
    ncontrols = problem.ncontrols

    parameterized_initial_value = problem.parameterized_initial_value
    parametric_rhs, control_regularizer, control = problem.parameterized_rhs
    objective_function = problem.objective_function
    lbu = problem.lbu
    ubu = problem.ubu
    mesh_width = problem.mesh_width

    nsamples = len(samples)
    nensemblestates = nstates*nsamples

    # ensemble right hand side
    ensemble_rhs, ensemble_initial_value = EnsembleRHS(parametric_rhs,
                        control_regularizer, control,
                        parameterized_initial_value,
                        samples, nstates, nensemblestates)

    integrator = RK4Integrator(ensemble_rhs, final_time, nintervals, nensemblestates, ncontrols)

    objective, constraints, decisions, initial_decisions, lbw, ubw, lbg, ubg = \
                                MultipleShootingOptimizationProblem(objective_function, integrator, lbu, ubu, 
                                ensemble_initial_value, alpha, nensemblestates, ncontrols, 
                                nsamples, nintervals)

    problem = {'f': objective, 'x': decisions, 'g': constraints}
    solver = nlpsol('solver', 'ipopt', problem);

    # Solve the NLP
    sol = solver(x0=initial_decisions, lbx=lbw, ubx=ubw, lbg=lbg, ubg=ubg)
    w_opt = sol['x'].full().flatten()

    return w_opt, sol['f']


if __name__ == "__main__":

    from harmonic_oscillator import HarmonicOscillator
    from plot_state_control import plot_state_control

    problem = HarmonicOscillator()

    w_opt = saa_problem(problem, [np.pi])
    plot_state_control(problem, w_opt, nsamples=1, date="")

