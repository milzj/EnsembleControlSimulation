import numpy as np
from casadi import *
from scipy.stats import qmc
from vaccination_scheduling import VaccinationScheduling

class Sampler(VaccinationScheduling):

    def __init__(self, nreplications=1):

        super().__init__()

        entropy = 0x3034c61a9ae04ff8cb62ab8ec2c4b501
        rng = np.random.default_rng(entropy)
        self.rngs = rng.spawn(nreplications)


    def sample(self, replication, nsamples, nparams):

        sigma = self.sigma
        nominal_param = self.nominal_param[0]

        sampler = qmc.Sobol(d=nparams, scramble=True, seed=self.rngs[replication])
        m = int(np.log2(nsamples))

        sample = sampler.random_base2(m=m)
    	sample = qmc.scale(sample, -1.0, 1.0)

        sample = (1+sigma*sample)*nominal_param

        return sample

if __name__ == "__main__":

    sampler = Sampler(nreplications=2)
    sample = sampler.sample(0, 4, 6)
    print(sample)
    print(len(sample))
    sample = sampler.sample(1, 4, 6)
    print(sample)
    print(len(sample))
