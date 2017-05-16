import time, os
from pathos.multiprocessing import ProcessingPool

class Harness(object):
    def __init__(self, func, sampler):
        self.func = func
        self.sampler = sampler

    def execute(self):
        arg_value_dict = self.sampler.sample()
        return self.func(**arg_value_dict)

    def execute_batch(self, n_samples):
        for _ in xrange(n_samples):
            self.execute()

SerialHarness = Harness

class PoolHarness(Harness):
    def __init__(self, func, sampler, n_processes):
        super(PoolHarness, self).__init__(func, sampler)
        self.n_processes = n_processes

    def execute_batch(self, n_samples):
        self.pool = ProcessingPool(self.n_processes)
        for _ in xrange(n_samples):
            arg_value_dict = self.sampler.sample()
            # XXX so the timestamp log dir can be distinct
            time.sleep(0.1)
            self.pool.apipe(self.func, **arg_value_dict)
        self.pool.close()
        self.pool.join()

class Sampler(object):
    def __init__(self, random_variables):
        self.random_variables = random_variables

    def sample(self):
        x = {}
        for rv in self.random_variables:
            x[rv.name] = rv.sample()
        return x

class LogDirSampler(Sampler):
    def __init__(self, random_variables, log_dir_argument_name=None, base_log_dir='log'):
        super(LogDirSampler, self).__init__(random_variables)
        self.log_dir_argument_name = log_dir_argument_name
        self.base_log_dir = base_log_dir

    def generate_log_dir(self):
        # use timestamps to generate unique directories for each run
        log_dir = os.path.join(self.base_log_dir, str(int(time.time() * 1e3)))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir

    def sample(self):
        x = super(LogDirSampler, self).sample()
        if self.log_dir_argument_name != None:
            x[self.log_dir_argument_name] = self.generate_log_dir()
        return x

if __name__ == '__main__':
    from distributions import Uniform, RandomVariable

    def f(x):
        print 'hi', x
    x = RandomVariable('x', Uniform(0, 1))
    s = Sampler([x])
    h = SerialHarness(f, s)
    for _ in xrange(100):
        h.execute()
