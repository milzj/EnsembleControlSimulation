from base import idx_state_control

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from casadi import *
from base.figure_style import *

def plot_state_control(problem, w_opt, nsamples=1, outdir="", filename="", ylim=[]):

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
    if ncontrols == 1:
        plt.plot(tgrid, vertcat(DM.nan(1), u1_opt), '-.',color="tab:blue", label=r"$u^*(t)$")
    if ncontrols == 2:
        plt.plot(tgrid, vertcat(DM.nan(1), u1_opt), '-.',color="tab:blue", label=r"$u_1^*(t)$")
        plt.plot(tgrid, vertcat(DM.nan(1), u2_opt), '--',color="tab:orange", label=r"$u_2^*(t)$")

    ax = plt.gca()

    if "reference" in filename and "harmonic_oscillator" in filename:
        # Split legend into control labels and parameter box
        control_handles, control_labels = ax.get_legend_handles_labels()
        control_legend = ax.legend(control_handles, control_labels, loc="upper left", bbox_to_anchor=(0.15, 1.0))
        ax.add_artist(control_legend)

        label = r"$\alpha = {}$".format(alpha) + "\n" + \
                r"$q = {}$".format(nintervals) + "\n" + \
                r"$N = {}$".format(nsamples)
        label = label.replace("N", "N_{\mathrm{ref}}")
        param_patch = mpatches.Patch(color='none', label=label)

        ax.legend(handles=[param_patch], loc="lower right")
    else:
        # Original single legend behavior
        handles, labels = ax.get_legend_handles_labels()

        if "reference" in filename:
            label = r"($\alpha={}, q = {}, N = {}$)".format(alpha,nintervals,nsamples)
            label = label.replace("N", "N_{\mathrm{ref}}")
        elif "nominal" in filename:
            label = r"($\alpha={}, q = {}$)".format(alpha,nintervals)
        else:
            label = r"($\alpha={}, q = {}, N={}$)".format(alpha,nintervals,nsamples)

        labels.append(label)
        handles.append(mpatches.Patch(color='none'))
        ax.legend(handles, labels)


    plt.xlabel(r'$t$')
    plt.grid()
    if ylim != []:
        #print(plt.ylim())
        plt.ylim(ylim)

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


