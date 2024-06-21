from base import idx_state_control
from base.figure_style import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from casadi import *



def plot_state_control(problem, w_opt, nsamples=1, outdir="", filename=""):

    nstates = problem.nstates
    alpha = problem.alpha
    nparams = problem.nparams
    ncontrols = problem.ncontrols
    nintervals = problem.nintervals
    mesh_width = problem.mesh_width
    nconstrols = problem.ncontrols

    idx_state, idx_control = idx_state_control(nstates, ncontrols, nsamples, nintervals)

    x1_opt = np.mean(w_opt[idx_state[0::nstates]], axis=0)
    x1_opt_std = np.std(w_opt[idx_state[0::nstates]], axis=0)

    x2_opt = np.mean(w_opt[idx_state[1::nstates]], axis=0)
    x2_opt_std = np.std(w_opt[idx_state[1::nstates]], axis=0)

    u1_opt = w_opt[idx_control[0::ncontrols]].flatten()
    if ncontrols > 1:
        u2_opt = w_opt[idx_control[1::ncontrols]].flatten()

    tgrid = [mesh_width*k for k in range(nintervals+1)]

    plt.figure(1)
    plt.clf()
    plt.plot(tgrid, vertcat(DM.nan(1), u1_opt), '-.',color="tab:orange", label=r"$u_1^*(t)$")
    if ncontrols > 1:
        plt.plot(tgrid, vertcat(DM.nan(1), u2_opt), '--',color="tab:blue", label=r"$u_2^*(t)$")

    handles, labels = plt.gca().get_legend_handles_labels() # get existing handles and labels
    empty_patch = mpatches.Patch(color='none') # create a patch with no color

    handles.append(empty_patch)  # add new patches and labels to list

    if filename.find("reference") != -1:
        label = r"($\alpha={}, n = {}, N = {}$)".format(alpha,nintervals,nsamples)
        label = label.replace("N", "N_{\mathrm{ref}}")
        labels.append(label)
    elif filename.find("nominal") != -1:
        labels.append(r"($\alpha={}, n = {}$)".format(alpha,nintervals))
    else:
        labels.append(r"($\alpha={}, n = {}, N={}$)".format(alpha,nintervals,nsamples))


    plt.legend(handles, labels) # apply new handles and labels to plot
    plt.xlabel(r'$t$')
    plt.grid()

    plt.gca().set_box_aspect(1)
    plt.tight_layout()

    plt.savefig(outdir+"/controls_{}.pdf".format(filename))

    plt.figure(1)
    plt.clf()
    plt.plot(tgrid, x1_opt, '--', label=r"$\mathbb{E}[x_1^*(t,\xi)]$", color="tab:blue")
    plt.plot(tgrid, x2_opt, '-', label=r"$\mathbb{E}[x_2^*(t,\xi)]$", color="tab:orange")
    plt.fill_between(tgrid,x1_opt-x1_opt_std, x1_opt+x1_opt_std, color="tab:blue", alpha=0.15, label=r"$\mathbb{E}[x_1^*(t,\xi)]\pm \mathrm{std}[x_1^*(t,\xi)]$")
    plt.fill_between(tgrid,x2_opt-x2_opt_std, x2_opt+x2_opt_std, color="tab:orange", alpha=0.15, label=r"$\mathbb{E}[x_2^*(t,\xi)]\pm \mathrm{std}[x_2^*(t,\xi)]$")
    plt.legend()
    plt.xlabel(r'$t$')
    plt.grid()
    plt.gca().set_box_aspect(1)
    plt.tight_layout()

    plt.savefig(outdir+"/states_{}.pdf".format(filename))


