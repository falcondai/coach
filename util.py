from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six

import os

def system_exec(base_command, _out_path=None, **arg_value_dict):
    sampled_args = []
    for arg_name, value in six.iteritems(arg_value_dict):
        sampled_args.append(' '.join(['--%s' % arg_name, str(value)]))
    cmd = ' '.join([base_command, ' '.join(sampled_args)])
    if _out_path is not None:
        with open(_out_path, 'ab') as f:
            f.write(cmd.encode('utf8'))
            f.write(b'\n')
    print(cmd)
    return os.system(cmd)

if __name__ == '__main__':
    system_exec('echo', **{'a': 1, 'b': 2})
