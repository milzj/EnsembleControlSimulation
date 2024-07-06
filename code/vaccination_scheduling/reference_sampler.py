from scipy.stats import qmc
from casadi import *
from .vaccination_scheduling import VaccinationScheduling

class ReferenceSampler(VaccinationScheduling):

    def __init__(self, nreplications):

        super().__init__()

        self.shift = 1000

        entropy = 0x3034c61a9ae04ff8cb62ab8ec2c4b501
        rng = np.random.default_rng(entropy)
        self.rngs = rng.spawn(self.shift+nreplications)


    def sample(self, nsamples, nparams, nreplication):

        n = nsamples
        if not (n & (n-1) == 0) and n != 0:
            raise ValueError("Sample size should be a power of 2.")

        seed = self.rngs[nreplication]
        sampler = qmc.Sobol(d=nparams, scramble=True, seed=seed)

        m = int(np.log2(nsamples))
        sample = sampler.random_base2(m=m)

        sample = self.scale(sample)

        return sample

    def scale(self, sample):

        sigma = self.sigma
        nominal_param = self.nominal_param[0]
        sample = (1+sigma*sample)*nominal_param

        return sample

if __name__ == "__main__":

    reference_sampler = ReferenceSampler(0)
    sample = reference_sampler.sample(16, 6, 0)
    print(sample)
    print(len(sample))
