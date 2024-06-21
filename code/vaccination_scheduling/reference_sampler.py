from scipy.stats import qmc
from casadi import *

class ReferenceSampler(object):

    def sample(self, nsamples, nparams, sigma=0.1, nominal_param=None):

        n = nsamples
        if not (n & (n-1) == 0) and n != 0:
            raise ValueError("Sample size should be a power of 2.")

        sampler = qmc.Sobol(d=nparams, scramble=False)

        m = int(np.log2(nsamples))

        sample = sampler.random_base2(m=m)
        sample = qmc.scale(sample, -1.0, 1.0)
        sample = (1+sigma*sample)*nominal_param

        return sample


if __name__ == "__main__":

    reference_sampler = ReferenceSampler()
    sample = reference_sampler.sample(4, 3, nominal_param=3*[1])
    print(sample)
    print(len(sample))
