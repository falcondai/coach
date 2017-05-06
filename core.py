import time, os

class Harness(object):
    def __init__(self, func, sampler):
        self.current_id = 0
        self.func = func
        self.sampler = sampler

    def execute(self):
        arg_value_dict = self.sampler.sample()
        self.current_id += 1
        return self.func(**arg_value_dict)

SerialHarness = Harness

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
