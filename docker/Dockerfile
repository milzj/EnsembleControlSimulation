FROM ubuntu:22.04

ENV DEB_PYTHON_INSTALL_LAYOUT=deb_system

# Install pip and git with apt
RUN apt-get update && \
    apt-get install -y python3-pip git

# We upgrade pip and setuptools
RUN python3 -m pip install --no-cache-dir pip setuptools --upgrade

ARG REPO_BRANCH="main"

WORKDIR /repo

# Copy pyproject.toml first so that we done need to reinstall in case another file
# is changing after rebuiding docker image
RUN git clone --branch ${REPO_BRANCH} --single-branch https://github.com/milzj/EnsembleControlSimulation.git
RUN cd EnsembleControlSimulation && python3 -m pip install --no-cache-dir -r requirements.txt && rm -rf /tmp
