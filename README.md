# Supplementary code for the manuscript: Convergence rates for ensemble-based solutions to optimal control of uncertain dynamical systems

[![DOI](https://zenodo.org/badge/806452621.svg)](https://zenodo.org/doi/10.5281/zenodo.12740932)

This repository contains supplementary code for the manuscript
> Olena Melnikov and Johannes Milz, 2024, 
> Convergence rates for ensemble-based solutions to optimal control of uncertain dynamical systems,
> https://doi.org/10.48550/arXiv.2407.18182

## Abstract

We consider optimal control problems involving nonlinear ordinary differential equations with uncertain inputs. By employing the sample average approximation, we obtain optimal control problems with ensembles of deterministic dynamical systems. Leveraging techniques for metric entropy bounds, we derive non-asymptotic Monte Carlo-type convergence rates for the ensemble-based solutions. Our theoretical framework is validated through numerical simulations on an academic optimal control problem and a vaccination scheduling problem for epidemic control under model parameter uncertainty.

## Using Docker

We provide a pre-build Docker image which can be used to run the code in this repository. First thing you need to do is to ensure that you have [docker installed](https://docs.docker.com/get-docker/).

To start an interactive docker container you can execute the following command

```bash
docker run --rm -it ghcr.io/milzj/ensembecontrolsimulation:latest
```

Alternatively, you can build a docker image locally and subsequently run it:

```bash
cd docker
docker build -t ensemblecontrolsimulation .
docker run -it ensemblecontrolsimulation
```

## Using without Docker

We recommend to create a virtual environment. After activating the venc, you can install the required packages via

```bash
pip install -r requirements.txt
```

## Running simulation

To run the simulations, execute

```bash
cd code
./simulate_problems.sh
```

## Postprocessing

To reproduce the figure for the nominal solution
of the harmonic oscillator, run

```bash
cd code
plot_nominal_control.py
```

### Notes

- The simulations included in the paper have been generated using Phython 3.10.14.
- Simulations were performed on a laptop equipped with a 12th Gen
440 Intel(R) Core(TM) i7-1260P processor and 16 GB of RAM.
- The simulation output included in the manuscript is located at
[code/output/06-Jul-2024-14-14-20](code/output/06-Jul-2024-14-14-20)
- We performed a replication study. The output is located in
[code/output/26-May-2025-12-13-44](code/output/26-May-2025-12-13-44).
The controls and convergence rates match those included in the paper.

## Having issues

If you have any troubles please file an issue in the GitHub repository.

## License

See [LICENSE](LICENSE).
