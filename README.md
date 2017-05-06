# coach
hyperparameter search for machine learning. A universal CLI tool that aims to simplify the dreaded hyperparameter search. It invokes your existing training script via shell.

## features
- support any training scripts
- support hyperparameter search methods:
  - random search
- support execution methods:
  - serial
- support argument distributions:
  - uniform
  - gaussian
  - log-uniform
  - discrete
- write sampled commands to file


## usage

### CLI
For random parameter search, we sample values for each argument according to the specified distribution.

example:
```bash
$ ./random_cli.py -n 10 \
  -d discrete_arg a 0.1 b 0.9 \
  -u uniform_arg1 0 10 -u uniform_arg2 10 100 \
  -g gaussian_arg 0 1 \
  'python train.py --max_iter 100'
```
This will serially execute 10 sampled commands. One of them might be
```bash
python train.py --max_iter 100 --gaussian_arg -1.71480724721 --uniform_arg2 25.1213987881 --uniform_arg1 3.91206703391 --discrete_arg b
```

### API
Though the design goal is to provide a universal CLI tool, the framework is written so it can also be used programmatically.

## author
Falcon Dai (me@falcondai.com)
