import numpy as np
from casadi import *
from scipy.stats import qmc
from vaccination_scheduling import ReferenceSampler

class Sampler(ReferenceSampler):

    def sample(self, replication, nsamples, nparams):

        sigma = self.sigma
        nominal_param = self.nominal_param[0]

        sample = self.rngs[self.shift+replication].uniform(0, 1.0, (nsamples, nparams))
        sample = self.scale(sample)

        return sample

if __name__ == "__main__":

    sampler = Sampler(nreplications=2)
    sample = sampler.sample(0, 4, 6)
    print(sample)
    print(len(sample))

