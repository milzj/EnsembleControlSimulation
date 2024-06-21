import numpy as np
from casadi import *
from scipy.stats import qmc

class Sampler(object):

    def __init__(self, nreplications=1):

        entropy = 0x3034c61a9ae04ff8cb62ab8ec2c4b501
        rng = np.random.default_rng(entropy)
        self.rngs = rng.spawn(nreplications)

    def sample(self, replication, nsamples, nparams, sigma=0.1, nominal_param=None):

        sample = self.rngs[replication].uniform(0.0, 1.0, (nsamples, nparams))
        sample = qmc.scale(sample, -1.0, 1.0)
        sample = (1+sigma*sample)*nominal_param

        return sample

if __name__ == "__main__":

    sampler = Sampler(nreplications=2)
    sample = sampler.sample(0, 4, 3, nominal_param=3*[1])
    print(sample)
    print(len(sample))

