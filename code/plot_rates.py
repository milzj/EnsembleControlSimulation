import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from base.figure_style import *
from base.lsqs_label import lsqs_label
import sys

from stats import load_dict, save_dict

def dict_to_mat(stats_dict):

    nx = len(list(stats_dict.keys()))
    ny = len(stats_dict[list(stats_dict.keys())[0]].keys())
    stats_mat = np.ones((nx, ny))

    i=-1
    for N in stats_dict.keys():
        vals = []
        i+=1
        j=-1
        for val in stats_dict[N].values():
            j+=1
            stats_mat[i, j] = val

    return stats_mat


def plot_rates(sample_sizes, errors, label, outdir, type, filename):

    plt.figure(1)
    plt.clf()

    # average
    plt.scatter(sample_sizes, np.mean(errors, axis=1), color="black", label=label)

    # realizations
    i=-1
    for N in sample_sizes:
        i+=1
        plt.scatter(N*np.ones(len(errors[i,:])), errors[i, :], marker="o", color="black", s=2, label="realizations")

    # least squares fit
    X = np.ones((len(sample_sizes),2))
    X[:,1] = np.log10(sample_sizes)
    x, residuals, rank, s = np.linalg.lstsq(X, np.log10(np.mean(errors, axis=1)), rcond=None)

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
    plt.savefig(outdir+"/{}={}.pdf".format(filename, type))


def plot_objective_rates(ref_date, saa_date, ndrop=1):

    # reference simulation
    outdir = "output/"+ref_date+"/harmonic_oscillator"
    filename = "reference_problem/harmonic_oscillator_optimal_values_{}".format(ref_date)
    ref_value = load_dict(outdir, filename)

    # SAA simulation
    outdir = "output/"+saa_date+"/harmonic_oscillator"
    filename = "saa_problem/harmonic_oscillator_optimal_values_{}".format(saa_date)
    saa_stats = load_dict(outdir, filename)

    # empirical means
    sample_sizes = list(saa_stats.keys())[ndrop::]
    stats_mat = dict_to_mat(saa_stats)
    errors = np.array(ref_value - stats_mat)

    errors = errors[ndrop::, :]

    # bias
    plot_rates(sample_sizes, errors, r"$v_{\mathrm{ref}}^*-\mathbb{E}[v_N^*]$", outdir, "bias_rates", filename)

    # l1
    plot_rates(sample_sizes, np.abs(errors), r"$\mathbb{E}[|v_N^*-v_{\mathrm{ref}}^*|]$",  outdir, "objective_rates", filename)

def plot_criticality_measures(saa_date, ndrop=1):

    # SAA simulation
    outdir = "output/"+saa_date+"/harmonic_oscillator"
    filename = "saa_problem/harmonic_oscillator_criticality_measures_{}".format(saa_date)
    saa_stats = load_dict(outdir, filename)

    # empirical means
    sample_sizes = list(saa_stats.keys())[ndrop::]
    stats_mat = dict_to_mat(saa_stats)
    errors = stats_mat[ndrop::,:]

    plot_rates(sample_sizes, errors, r"$\chi$", outdir, "criticality_measure_rates", filename)


if __name__ == "__main__":

    ref_date = sys.argv[1]
    saa_date = sys.argv[2]

    ndrop = 0
    plot_objective_rates(ref_date, saa_date, ndrop=ndrop)
    plot_criticality_measures(saa_date, ndrop=ndrop)
