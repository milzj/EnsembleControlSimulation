import numpy as np
import matplotlib


from casadi import *

final_time = 1. # Time horizon
nintervals = 4 # ncontrolsmber of control intervals
alpha = 1e-3
lbu = [-3.,-3.]
ubu = [3.,3.]

def parameterized_initial_value(params):
  # parameterized initial value
  return [1.0,0.0]

nominal_param = [np.pi]
nsamples = 3 # sample size
nreplications = 1

def objective_function(x):
  # Objective function to be evaluated
  # at states at final time
  # Notation F in manuscript
  return x[0]**2 + x[1]**2

mesh_width = final_time/nintervals
nparams = len(nominal_param)
nstates = len(parameterized_initial_value(nparams*[0]))
ncontrols = len(lbu)
nensemblestates = nstates*nsamples

# Declare model variables
x = MX.sym('x', nstates)
u = MX.sym('u', ncontrols)
k = MX.sym('k', nparams)

# Model equations
xdot = vertcat(-k[0]*x[1]+u[0], k[0]*x[0]+u[1])

# Objective term
L = u[0]**2+u[1]**2

# parameterized right-hand side
ParametricRHS = Function('fp', [x, u, k], [xdot])
Y = MX.sym('Y', nensemblestates)

entropy = 0x3034c61a9ae04ff8cb62ab8ec2c4b501
rng = np.random.default_rng(entropy)
rngs = rng.spawn(nreplications)

samples = rngs[0].uniform(0, 2*nominal_param[0], (nsamples, nparams))

# ensemble right hand side
ensemble_initial_value = []
Ydot = []

for i in range(nsamples):
  params = samples[i]
  idx = np.arange(nstates)+i*nstates
  ydot = ParametricRHS(Y[idx], u, params)
  Ydot = vertcat(Ydot, ydot)
  ensemble_initial_value += parameterized_initial_value(params)

EnsembleRHS = Function('ensembleRHS', [Y, u], [Ydot, L])

EnsembleRHS(ensemble_initial_value, lbu)

def Integrator(rhs, final_time, nintervals, nstates, ncontrols, steps_per_interval=4):
  # Fixed step Runge-Kutta 4 integrator
  # Adapted from https://github.com/casadi/casadi/blob/main/docs/examples/python/direct_multiple_shooting.py
  DT = final_time/nintervals/steps_per_interval
  X0 = MX.sym('X0', nstates)
  U = MX.sym('U', ncontrols)
  X = X0
  Q = 0.0
  for j in range(steps_per_interval):
    k1, k1_q = rhs(X, U)
    k2, k2_q = rhs(X + DT/2 * k1, U)
    k3, k3_q = rhs(X + DT/2 * k2, U)
    k4, k4_q = rhs(X + DT * k3, U)
    X = X + DT/6*(k1 +2*k2 +2*k3 +k4)
    Q = Q + DT/6*(k1_q + 2*k2_q + 2*k3_q + k4_q)
  integrator = Function('integrator', [X0, U], [X, Q],['x0','p'],['xf','qf'])
  return integrator

integrator = Integrator(EnsembleRHS, final_time, nintervals, nensemblestates, ncontrols)

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
Xk  = MX.sym('X0', nensemblestates)
w   += [Xk]
lbw += ensemble_initial_value
ubw += ensemble_initial_value
w0  += ensemble_initial_value

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

    # New NLP variable for state at end of interval
    Xk = MX.sym('X_' + str(k+1), nensemblestates)
    w   += [Xk]
    lbw += nensemblestates*[-inf]
    ubw += nensemblestates*[inf]
    w0  += nsamples*parameterized_initial_value(nparams*[0])

    # Add equality constraint
    g   += [Xk_end-Xk]
    lbg += nensemblestates*[0.0]
    ubg += nensemblestates*[0.0]

J *= (alpha/2.0)

for i in range(nsamples):
  idx = np.arange(nstates)+i*nstates
  # TODO: Improve implementation of averaging
  J += objective_function(Xk[idx])/nsamples

#J *= 1./mesh_width

objective = J
constraints = vertcat(*g)
decisions = vertcat(*w)

# Create an NLP solver
problem = {'f': objective, 'x': decisions, 'g': constraints}
solver = nlpsol('solver', 'ipopt', problem);

# Solve the NLP
sol = solver(x0=w0, lbx=lbw, ubx=ubw, lbg=lbg, ubg=ubg)
w_opt = sol['x'].full().flatten()

def idx_state_control(nstates, ncontrols, nsamples, nintervals):
  # Compute

  idx = np.arange((nstates*nsamples+ncontrols)*(nintervals+1))
  idx = idx.reshape((nstates*nsamples+ncontrols, nintervals+1), order='F')
  idx_state = idx[0:nstates*nsamples, :]
  idx_control = idx[nstates*nsamples:nstates*nsamples+ncontrols+1, 0:nintervals]

  return idx_state, idx_control

idx_state, idx_control = idx_state_control(nstates, ncontrols, nsamples, nintervals)

x1_opt = np.mean(w_opt[idx_state[0::nstates]], axis=0)
x1_opt_std = np.std(w_opt[idx_state[0::nstates]], axis=0)

x2_opt = np.mean(w_opt[idx_state[1::nstates]], axis=0)
x2_opt_std = np.std(w_opt[idx_state[1::nstates]], axis=0)

u1_opt = w_opt[idx_control[0::ncontrols]].flatten()
u2_opt = w_opt[idx_control[1::ncontrols]].flatten()

tgrid = [mesh_width*k for k in range(nintervals+1)]

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.rcParams.update({
    'font.size': 8,
    'text.usetex': True,
    'text.latex.preamble': r'\usepackage{amsfonts}'
})

plt.figure(1)
plt.clf()
plt.plot(tgrid, vertcat(DM.nan(1), u1_opt), '-.',color="tab:orange", label=r"$u_1^*(t)$")
plt.plot(tgrid, vertcat(DM.nan(1), u2_opt), '--',color="tab:blue", label=r"$u_2^*(t)$")

handles, labels = plt.gca().get_legend_handles_labels() # get existing handles and labels
empty_patch = mpatches.Patch(color='none') # create a patch with no color

handles.append(empty_patch)  # add new patches and labels to list
labels.append(r"($\alpha={}, n={}, N={}$)".format(alpha,nintervals,nsamples))

plt.legend(handles, labels) # apply new handles and labels to plot
plt.xlabel(r'$t$')
plt.grid()
plt.show()

plt.figure(1)
plt.clf()
plt.plot(tgrid, x1_opt, '--', label=r"$\mathbb{E}[x_1^*(t,\xi)]$", color="tab:blue")
plt.plot(tgrid, x2_opt, '-', label=r"$\mathbb{E}[x_2^*(t,\xi)]$", color="tab:orange")
plt.fill_between(tgrid,x1_opt-x1_opt_std, x1_opt+x1_opt_std, color="tab:blue", alpha=0.15, label=r"$\mathbb{E}[x_1^*(t,\xi)]\pm \mathrm{std}[x_1^*(t,\xi)]$")
plt.fill_between(tgrid,x2_opt-x2_opt_std, x2_opt+x2_opt_std, color="tab:orange", alpha=0.15, label=r"$\mathbb{E}[x_2^*(t,\xi)]\pm \mathrm{std}[x_2^*(t,\xi)]$")
plt.legend()
plt.xlabel(r'$t$')
plt.grid()
plt.show()
