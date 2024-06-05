import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from style.figure_style import *
from style.lsqs_label import lsqs_label
import sys

from stats import load_dict, save_dict

def plot_objective_rates(ref_date, saa_date, ndrop=1):

    # reference simulation
    outdir = "output/"+ref_date+"/harmonic_oscillator"
    filename = "reference_problem/harmonic_oscillator_optimal_values_{}".format(ref_date)
    ref_value = load_dict(outdir, filename)

    # SAA simulation
    outdir = "output/"+saa_date+"/harmonic_oscillator"
    filename = "harmonic_oscillator_optimal_values_{}".format(saa_date)
    saa_stats = load_dict(outdir, filename)

    plt.figure(1)
    plt.clf()

    # empirical means
    sample_sizes = list(saa_stats.keys())
    sample_sizes = sample_sizes[ndrop::]
    errors = []
    for N in sample_sizes:
        vals = []
        for val in saa_stats[N].values():
            vals += [ref_value-val]
        error = np.mean(vals)
        errors += [error]

    plt.scatter(sample_sizes, errors, color="black", label=r"$v_{\mathrm{ref}}^*-\mathbb{E}[v_N^*]$")

    # least squares fit
    X = np.ones((len(sample_sizes),2))
    X[:,1] = np.log10(sample_sizes)
    x, residuals, rank, s = np.linalg.lstsq(X, np.log10(errors), rcond=None)

    rate = x[1]
    constant = 10.0**x[0]

    plt.plot(sample_sizes, constant*sample_sizes**rate, color="black", linestyle="--", label=lsqs_label(rate=rate, constant=constant, base="N"))

    _handles, _labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(_labels, _handles))
    plt.legend(by_label.values(), by_label.keys(), loc="best")

    plt.xscale("log", base=2)
    plt.yscale("log", base=2)
    plt.xlabel(r'sample size $N$')
    plt.gca().set_box_aspect(1)
    plt.tight_layout()
    plt.savefig(outdir+"/bias_rates={}.pdf".format(filename))

    plt.figure(1)
    plt.clf()

    # realizations
    Errors = []
    for N in sample_sizes:
        errors = []
        for error in saa_stats[N].values():
            errors += [np.abs(error-ref_value)]
        Errors += [np.mean(errors)]
        plt.scatter(N, np.mean(errors), marker="s", color="black", label=r"$\mathbb{E}[|v_N^*-v_{\mathrm{ref}}^*|]$")
        plt.scatter(N*np.ones(len(errors)), errors, marker="o", color="black", s=2, label="realizations")

    print(Errors)
    # least squares fit
    X = np.ones((len(sample_sizes),2))
    X[:,1] = np.log10(sample_sizes)
    x, residuals, rank, s =np.linalg.lstsq(X, np.log10(Errors), rcond=None)

    rate = x[1]
    constant = 10.0**x[0]

    plt.plot(sample_sizes, constant*sample_sizes**rate, color="black", linestyle="--", label=lsqs_label(rate=rate, constant=constant, base="N"))

    _handles, _labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(_labels, _handles))
    plt.legend(by_label.values(), by_label.keys(), loc="best")


    plt.xscale("log", base=2)
    plt.yscale("log", base=2)
    plt.xlabel(r'sample size $N$')
    plt.gca().set_box_aspect(1)
    plt.tight_layout()
    plt.savefig(outdir+"/objective_rates={}.pdf".format(filename))




if __name__ == "__main__":

    ref_date = sys.argv[1]
    saa_date = sys.argv[2]

    plot_objective_rates(ref_date, saa_date)
