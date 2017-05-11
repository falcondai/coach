#!/usr/bin/env python

import numpy as np
import os, sys, pickle
from util import system_exec
from distributions import RandomVariable, Uniform, Gaussian, Discrete, LogUniform
from core import SerialHarness, PoolHarness, LogDirSampler

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', help='base command string')
    parser.add_argument('-n', '--n-samples', default=4, type=int, help='number of experiments to run')
    parser.add_argument('-s', '--save-cmds-to', help='saves sampled commands to a file')
    parser.add_argument('--log-arg', help='the log directory argument name')
    parser.add_argument('-b', '--base-log-dir', default='/tmp', help='the base directory for log files')
    parser.add_argument('-p', '--pool-size', type=int, default=1, help='the size of the worker pool, i.e. how many commands are executed in parallel')

    parser.add_argument('-u', '--uniform', nargs=3, metavar=('full_argument_name', 'lower_bound', 'upper_bound'), action='append', help='uniformly distributed input values')
    parser.add_argument('-g', '--gaussian', nargs=3, metavar=('full_argument_name', 'mean', 'variance'), action='append', help='normally distributed input values')
    parser.add_argument('-l', '--log-uniform', nargs=3, metavar=('full_argument_name', 'lower_bound', 'upper_bound'), action='append', help='log uniformly distributed input values')
    parser.add_argument('-d', '--discrete', nargs='+', action='append', help='full argument name, value_1, likelihood for value_1, value_2, ... . for multinomially distributed input values')

    args = parser.parse_args()

    # parse arguments
    rvs = []
    if args.uniform is not None:
        for arg_tuple in args.uniform:
            name = arg_tuple[0]
            rv = RandomVariable(name, Uniform.parse(arg_tuple[1:]))
            rvs.append(rv)
    if args.gaussian is not None:
        for arg_tuple in args.gaussian:
            name = arg_tuple[0]
            rv = RandomVariable(name, Gaussian.parse(arg_tuple[1:]))
            rvs.append(rv)
    if args.log_uniform is not None:
        for arg_tuple in args.log_uniform:
            name = arg_tuple[0]
            rv = RandomVariable(name, LogUniform.parse(arg_tuple[1:]))
            rvs.append(rv)
    if args.discrete is not None:
        for arg_tuple in args.discrete:
            name = arg_tuple[0]
            rv = RandomVariable(name, Discrete.parse(arg_tuple[1:]))
            rvs.append(rv)

    if args.save_cmds_to is not None:
        fo = open(args.save_cmds_to, 'a')
    else:
        fo = sys.stdout
    sampler = LogDirSampler(rvs, log_dir_argument_name=args.log_arg, base_log_dir=args.base_log_dir)
    f = lambda **kwargs: system_exec(args.command, fo, **kwargs)
    harness = SerialHarness(f, sampler) if args.pool_size == 1 else PoolHarness(f, sampler, args.pool_size)
    harness.execute_batch(args.n_samples)
