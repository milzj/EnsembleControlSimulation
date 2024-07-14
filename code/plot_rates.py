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


def plot_rates(sample_sizes, errors, label, label_realizations, outdir, type, filename, errorfct=lambda x : np.mean(x, axis=1)):

    plt.figure(1)
    plt.clf()

    # average
    plt.scatter(sample_sizes, errorfct(errors), color="black", label=label)

    # realizations
    i=-1
    for N in sample_sizes:
        i+=1
        plt.scatter(N*np.ones(len(errors[i,:])), errors[i, :], marker="o", color="black", s=2, label=label_realizations)

    # least squares fit
    X = np.ones((len(sample_sizes),2))
    X[:,1] = np.log10(sample_sizes)
    x, residuals, rank, s = np.linalg.lstsq(X, np.log10(errorfct(errors)), rcond=None)

    rate = x[1]
    constant = 10.0**x[0]
    plt.plot(sample_sizes, constant*np.array(sample_sizes)**rate, color="black", linestyle="--", label=lsqs_label(rate=rate, constant=constant, base="N"))

    _handles, _labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(_labels, _handles))
    plt.legend(by_label.values(), by_label.keys(), loc="best")

    plt.xscale("log", base=2)
    plt.yscale("log", base=2)
    plt.xlabel(r'sample size $N$')
    plt.gca().set_box_aspect(1)
    plt.tight_layout()
    plt.savefig(outdir+"/{}={}.pdf".format(filename, type))


def plot_objective_rates(ref_date, saa_date, name, nrefrepliations, ndrop=1):

    # reference simulation
    outdir = "output/"+ref_date+"/"+name
    ref_value = []
    for nreplication in range(nrefreplications):
        filename = "reference_problem/"+name+"_optimal_values_rep_{}_{}".format(nreplication, ref_date)
        ref_value += [load_dict(outdir, filename)]
    ref_value = np.mean(ref_value)

    # SAA simulation
    outdir = "output/"+saa_date+"/"+name
    filename = "saa_problem/"+name+"_optimal_values_{}".format(saa_date)
    saa_stats = load_dict(outdir, filename)

    # empirical means
    sample_sizes = list(saa_stats.keys())[ndrop::]
    stats_mat = dict_to_mat(saa_stats)
    errors = np.array(ref_value - stats_mat)
    errors = errors[ndrop::, :]

    # bias
    label_realizations =  r"$v_{\mathrm{ref}}^*-v_N^*$"
    plot_rates(sample_sizes, errors, "$v_{\mathrm{ref}}^*-\widehat{\mathbb{E}}[v_N^*]$", label_realizations, outdir, "bias_rates", filename)

    # l1
    label_realizations =  r"$|v_N^*-v_{\mathrm{ref}}^*|$"
    plot_rates(sample_sizes, np.abs(errors), r"$\widehat{\mathbb{E}}[|v_N^*-v_{\mathrm{ref}}^*|]$",  label_realizations, outdir, "objective_rates", filename, )

    # rmse
    errorfct = lambda x : np.sqrt(np.mean(x**2, axis=1))
    label_realizations =  r"$|v_N^*-v_{\mathrm{ref}}^*|$"
    plot_rates(sample_sizes, np.abs(errors), r"$(\widehat{\mathbb{E}}[|v_N^*-v_{\mathrm{ref}}^*|^2])^{1/2}$",  label_realizations, outdir, "rmse_rates", filename, errorfct=errorfct)

    # std
    errorfct = lambda x : np.sqrt(np.mean(x**2, axis=1))
    errors = (stats_mat.transpose() - np.mean(stats_mat, axis=1)).transpose()
    errors = errors[ndrop::, :]

    label_realizations =  r"$|v_N^*-\widehat{\mathbb{E}}[v_N^*]|$"
    plot_rates(sample_sizes, errors, r"$(\widehat{\mathbb{E}}[|v_N^*-\widehat{\mathbb{E}}[v_N^*]|^2])^{1/2}$", label_realizations, outdir, "std_rates", filename, errorfct=errorfct)

def plot_criticality_measures(saa_date, name, nreplications, ndrop=1):

    # SAA simulation
    outdir = "output/"+saa_date+"/"+name
    filename = "saa_problem/"+name+"_criticality_measures_rep_{}".format(saa_date)
    saa_stats = load_dict(outdir, filename)
    stats_mat = dict_to_mat(saa_stats)


    # empirical means
    sample_sizes = list(saa_stats.keys())[ndrop::]
    errors = stats_mat[ndrop::,:]

    label_realizations =  r"$\chi_{\mathrm{ref}}(u_N^*)$"
    plot_rates(sample_sizes, errors, r"$\widehat{\mathbb{E}}[\chi_{\mathrm{ref}}(u_N^*)]$", label_realizations, outdir, "criticality_measure_rates", filename)


if __name__ == "__main__":

    ref_date = sys.argv[1]
    saa_date = sys.argv[2]
    name = sys.argv[3]
    ndrop = int(sys.argv[4])
    nrefreplications = int(sys.argv[5])

    plot_objective_rates(ref_date, saa_date, name, nrefreplications, ndrop=ndrop)
    plot_criticality_measures(saa_date, name, nrefreplications, ndrop=ndrop)
