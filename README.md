# Supplementary code for the manuscript: Convergence rates for ensemble-based solutions to optimal control of uncertain dynamical systems

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/milzj/EnsembleControlSimulation/HEAD)

This repository contains supplementary code for the manuscript
> Olena Melnikov and Johannes Milz, 2024, 
> Convergence rates for ensemble-based solutions to optimal control of uncertain dynamical systems

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

## Running simulation

To run the simulations, execute

```bash
cd code
./simulate_problems.sh
```

## Postprocessing

To the reproduce figure for the nominal solution
of the harmonic oscillator, run

```bash
cd code
plot_nominal_control.py
```

## Having issues

If you have any troubles please file an issue in the GitHub repository.

## License

See [LICENSE](LICENSE).
