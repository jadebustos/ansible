#!/usr/bin/env python

# (c) 2015 Jose Angel de Bustos Perez <jadebustos@gmail.com>
# Script to run an ansible runner using a module (ansible 1.9)

# From the controller machine, where this script is executed, to the nodes
# ssh has to be carried out without password (using rsa keys, by example).

# This file shows how to execute an ansible module, custom remote-cmd module.
# Dynamic ansible inventory is used.

import json
import ansible.runner
import ansible.inventory

def exec_runner(hosts):

    # Hosts where execute commands
    example_host1 = ansible.inventory.host.Host(name=hosts[0])
    example_host2 = ansible.inventory.host.Host(name=hosts[1])

    # Setting hosts group
    task_group = ansible.inventory.group.Group(name="test")

    # Hosts added to group
    task_group.add_host(example_host1)
    task_group.add_host(example_host2)

    # Inventory
    task_inventory = ansible.inventory.Inventory()
    task_inventory.add_group(task_group)
    task_inventory.subset('test')

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
	# dynamic inventory
        inventory=task_inventory,
    )

    # Executing module on nodes
    response = runner.run()

    # Modules output is a json
    return response

if __name__ == '__main__':

    # hosts where execute commands
    hosts = ['ansible01.ad.jadbp.lab', 'ansible02.ad.jadbp.lab']

    res = exec_runner(hosts)

    # dark <- not contacted hosts
    # contacted <- contacted hosts
    print json.dumps(res, indent=4)
