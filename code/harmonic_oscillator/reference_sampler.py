from scipy.stats import qmc
from casadi import *

class ReferenceSampler(object):

    def sample(self, nsamples, nparams):

        n = nsamples
        if not (n & (n-1) == 0) and n != 0:
            raise ValueError("Sample size should be a power of 2.")

        sampler = qmc.Sobol(d=nparams, scramble=False)

        m = int(np.log2(nsamples))
        sample = sampler.random_base2(m=m)

        return self.scale(sample)

    def scale(self, sample):
        """Scale (0,1) samples"""

        sample[:,1:] *= 2.
        sample[:,1:] -= 1.
        sample[:,1:3] *= 5.
        sample[:,3:5] *= .25

        return sample



if __name__ == "__main__":

    reference_sampler = ReferenceSampler()
    sample = reference_sampler.sample(4, 3)
    print(sample)
    print(len(sample))
