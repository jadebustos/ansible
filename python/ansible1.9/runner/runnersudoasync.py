#!/usr/bin/env python

# (c) 2015 Jose Angel de Bustos Perez <jadebustos@gmail.com>
# Script to run an ansible runner using a module (ansible 1.9)
#
# From the controller machine, where this script is executed, to the nodes
# ssh has to be carried out without password (using rsa keys, by example).
#
# This file shows how to execute a sudo remote command in async mode.
# custom remote-cmd module is used.
# stdout and stderr from the remote command are placed in:
#   /home/remoteuser/.ansible_async/jobid
# This file is copied from the remote node to the controller to:
#   /tmp/hostname/home/remoteuser/.ansible_async/jobid
# After copying the file is removed from the remote machine.

# This script uses kerberos authentication. To use that ssh native
# client need to be supported. If ssh native client is not supported 
# then pub key authentication or password authentication must be used.

import json
import ansible.runner
import ansible.inventory
import subprocess
import sys

def exec_runner(hosts):

    sshUser = 'jadebustos'
    # Uncomment this to increase verbosity
    #ansible.utils.VERBOSITY = 4

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
        module_args='/usr/bin/python /root/test.py',
        remote_user=sshUser,
        pattern=':'.join(hosts),
        # Task hard limit, if task has not finished after background seconds task will be finished
	background=20,
        inventory=task_inventory,
    )

    # This script uses kerberos authentication. To use that ssh native
    # client need to be supported. If ssh native client is not supported 
    # then pub key authentication or password authentication must be used.
    krbCmd = "/usr/bin/kinit -kt /root/jadebustos.keytab jadebustos"
    execKrbCmd = subprocess.Popen(krbCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    myStdout, myStderr = execKrbCmd.communicate()

    # Executing module on nodes in async mode
    response, poller = runner.run_async(20)
    # Wait until task is finished, hard time is set to 20 and polling is carried out every 8 seconds
    poller.wait(20, 8)
   
    items = response['contacted'].keys()

    # Results file for each task y copied to /tmp/hostname/username/.ansible_async/taskid 
    for item in items:
      print "Procesando: " + item
      resFile = response['contacted'][item]['results_file']
      # Runner to get remote results file to /tmp
      runnerFile = ansible.runner.Runner(
        module_name='fetch',
        module_args='src=' + resFile + ' dest=/tmp/ fail_on_missing=no flat=no',
        remote_user=sshUser,
        pattern=item,
        inventory=task_inventory,
      )
      runnerFile.run()
      # Runner to remove remote results file
      runnerDelFile = ansible.runner.Runner(
        module_name='file',
        module_args='path=' + resFile + ' state=absent',
      
        remote_user=sshUser,
        pattern=item,
        inventory=task_inventory,
      )
      runnerDelFile.run()

    # Modules output is a json
    return response

if __name__ == '__main__':

    # hosts where execute commands
    hosts = ['ansible01.ad.jadbp.lab', 'ansible02.ad.jadbp.lab']

    res = exec_runner(hosts)

    # dark <- not contacted hosts
    # contacted <- contacted hosts
    print json.dumps(res, indent=4)
