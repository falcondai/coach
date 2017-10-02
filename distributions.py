from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from six.moves import xrange

import numpy as np


class Distribution(object):
    def __init__(self):
        raise NotImplementedError

    def sample(self):
        raise NotImplementedError

    @staticmethod
    def parse(args):
        '''
        Args:
            args (list): a list of strings to be parsed as arguments for the distribution.
        Returns:
            Distribution: a distribution instantiated by parsed args.
        '''
        raise NotImplementedError


class RandomVariable(object):
    def __init__(self, name, distribution):
        self.name = name
        self.distribution = distribution

    def sample(self):
        return self.distribution.sample()


class Uniform(Distribution):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def sample(self):
        return np.random.uniform(self.lower, self.upper)

    @staticmethod
    def parse(args):
        assert len(args) == 2, '%r should be the lower and upper bounds.' % args
        lower, upper = args
        lower = float(lower)
        upper = float(upper)
        return Uniform(lower, upper)


class Gaussian(Distribution):
    def __init__(self, mean, variance):
        self.mean = mean
        self.variance = variance

    def sample(self):
        return np.random.normal(self.mean, self.variance)

    @staticmethod
    def parse(args):
        assert len(args) == 2, '%r should be the mean and variance.' % args
        mean, variance = args
        mean = float(mean)
        variance = float(variance)
        return Gaussian(mean, variance)


class LogUniform(Distribution):
    def __init__(self, lower, upper):
        self.log_lower = np.log(lower)
        self.log_upper = np.log(upper)

    def sample(self):
        return np.exp(np.random.uniform(self.log_lower, self.log_upper))

    @staticmethod
    def parse(args):
        assert len(args) == 2, '%r should be the lower and upper bounds.' % args
        lower, upper = args
        lower = float(lower)
        upper = float(upper)
        return Uniform(lower, upper)


class Discrete(Distribution):
    def __init__(self, value_prob_dict):
        self.values = value_prob_dict.keys()
        self.probs = value_prob_dict.values()
        assert np.sum(self.probs) == 1, 'total probability must sum to 1.'

    def sample(self):
        return np.random.choice(self.values, p=self.probs)

    @staticmethod
    def parse(args):
        assert len(args) % 2 == 0, '%r must form pairs of (x, p_x).' % args
        n_pairs = len(args) / 2
        value_prob_dict = {}
        for i in xrange(n_pairs):
            x, px = args[2 * i:2 * i + 2]
            value_prob_dict[x] = float(px)
        return Discrete(value_prob_dict)


if __name__ == '__main__':
    u = Uniform.parse([0, 1])
    print(u.sample())
