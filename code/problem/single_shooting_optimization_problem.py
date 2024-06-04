from casadi import *


def SingleShootingOptimizationProblem(objective_function, integrator, lbu, ubu, 
                initial_value, alpha, nstates, ncontrols, nsamples, nintervals):
    # Start with an empty NLP
    # Adapted from https://github.com/casadi/casadi/blob/main/docs/examples/python/direct_multiple_shooting.py
    w=[]
    w0 = []
    lbw = []
    ubw = []
    J = 0.0
    g=[]
    lbg = []
    ubg = []

    # "Lift" initial conditions
    Xk  = MX.sym('X0', nstates)

    # Formulate the NLP
    for k in range(nintervals):
        # New NLP variable for the control
        Uk = MX.sym('U_' + str(k), ncontrols)
        w   += [Uk]
        lbw += lbu
        ubw += ubu
        w0  += lbu

        # Integrate till the end of the interval
        Fk = integrator(x0=Xk, p=Uk)
        Xk_end = Fk['xf']
        J += Fk['qf']

    J *= (alpha/2.0)

    for i in range(nsamples):
      idx = np.arange(nstates // nsamples)+i*(nstates // nsamples)
      # TODO: Improve implementation of averaging
      J += objective_function(Xk[idx])/nsamples

    #J *= 1./mesh_width

    objective = J
    constraints = vertcat(*g)
    decisions = vertcat(*w)

    return objective, constraints, decisions, w0, lbw, ubw, lbg, ubg
