from scipy.stats import qmc
from casadi import *

class ReferenceSampler(object):

    def __init__(self, nreplications):

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

        return self.scale(sample)

    def scale(self, sample):
        """Scale (0,1) samples"""

        sample[:,1:] *= 2.
        sample[:,1:] -= 1.
        sample[:,1:3] *= 5.
        sample[:,3:5] *= .5

        return sample



if __name__ == "__main__":

    reference_sampler = ReferenceSampler(1)
    sample = reference_sampler.sample(4, 3, 0)
    print(sample)

    sample = reference_sampler.sample(4, 3, 1)
    print(sample)
