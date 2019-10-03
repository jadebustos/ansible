#!/usr/bin/env python

# (c) 2015 Jose Angel de Bustos Perez <jadebustos@gmail.com>
# Script to run an ansible runner using a module (ansible 1.9)

# From the controller machine, where this script is executed, to the nodes
# ssh has to be carried out without password (using rsa keys, by example).

# This file shows how to execute an ansible module, custom remote-cmd module.
# Ansible inventory is used. Placed in /etc/ansible/hosts file.

import json
import ansible.runner


def exec_runner(hosts):

    # Runner
    runner = ansible.runner.Runner(
        # remote-cmd.py must be in ansible library path or in the library directory
        # inside the directory where this script is placed
        module_name='remote-cmd',
        # the command to be executed on remote hosts must be passed as an argument
        # to the module
        module_args='/root/test.py',
        remote_user='root',
        pattern=':'.join(hosts),
    )

    # Executing module on nodes
    response = runner.run()

    # Modules output is a json
    return response

if __name__ == '__main__':

    # hosts where execute commands, these hosts have to be defined in ansible's
    # inventory (/etc/ansible/hosts)
    hosts = ['ansible01.ad.jadbp.lab', 'ansible02.ad.jadbp.lab']

    res = exec_runner(hosts)

    # dark <- not contacted hosts
    # contacted <- contacted hosts
    print json.dumps(res, indent=4)
