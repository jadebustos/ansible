#!/usr/bin/python

# (c) 2015 Jose Angel de Bustos Perez <jadebustos@gmail.com>
# Script to execute an ansible playbook (ansible 1.9)

# From the controller machine, where this script is executed, to the nodes
# ssh has to be carried out without password (using rsa keys, by example).

import ansible.runner
import ansible.playbook
import ansible.inventory
from ansible import callbacks
from ansible import utils
import json
import traceback


def exec_playbook(cmd):

    # Hosts where execute commands
    example_host1 = ansible.inventory.host.Host(name="ansible01.ad.jadbp.lab")
    example_host2 = ansible.inventory.host.Host(name="ansible02.ad.jadbp.lab")

    # Setting variables
    example_host1.set_variable('cmd', cmd)
    example_host2.set_variable('cmd', cmd)

    # ANSIBLE_SSH_ARGS??? como variable??

    # Setting remote user (in ansible 2.0 ssh_user must be used)
    example_host1.set_variable('ansible_ssh_user', 'jadebustos')
    example_host2.set_variable('ansible_ssh_user', 'jadebustos')

    # Setting hosts group
    task_group = ansible.inventory.group.Group(name="test")

    # Hosts added to group
    task_group.add_host(example_host1)
    task_group.add_host(example_host2)

    # Inventory
    task_inventory = ansible.inventory.Inventory()
    task_inventory.add_group(task_group)
    task_inventory.subset('test')

    # Callbacks
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    # Playbook
    # https://github.com/ansible/ansible/blob/release1.8.4/lib/ansible/playbook/__init__.py#L42-L84
    try:
        pb = ansible.playbook.PlayBook(playbook="ansible-template.yml",
                                       stats=stats,
                                       callbacks=playbook_cb,
                                       runner_callbacks=runner_cb,
                                       inventory=task_inventory,
                                       check=True)

        pr = pb.run()
    except:
        print traceback.format_exc()

# Another way to get information
#    hosts = sorted(pb.stats.processed.keys())
#    for h in hosts:
#       print ', '.join(pb.stats.summarize(h).keys())

    return pr

if __name__ == '__main__':

    # Command to be executed remotely
    cmd = '/usr/bin/python /root/test.py'

    res = exec_playbook(cmd)

    print json.dumps(res, indent=4)

