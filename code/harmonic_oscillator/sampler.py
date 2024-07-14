import numpy as np
from casadi import *
from scipy.stats import qmc
from harmonic_oscillator import ReferenceSampler

class Sampler(ReferenceSampler):

    def sample(self, replication, nsamples, nparams):

        sample = self.rngs[self.shift+replication].uniform(0, 1.0, (nsamples, nparams))
        return self.scale(sample)

if __name__ == "__main__":

    sampler = Sampler(nreplications=2)
    sample = sampler.sample(0, 4, 3)
    print(sample)
    print(len(sample))

