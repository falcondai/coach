import os

def system_exec(base_command, _out_file=None, **arg_value_dict):
    sampled_args = []
    for arg_name, value in arg_value_dict.iteritems():
        sampled_args.append(' '.join(['--%s' % arg_name, str(value)]))
    cmd = ' '.join([base_command, ' '.join(sampled_args)])
    if _out_file is not None:
        _out_file.write(cmd)
        _out_file.write('\n')
    return os.system(cmd)

if __name__ == '__main__':
    system_exec('echo', **{'a': 1, 'b': 2})
