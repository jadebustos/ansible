#!/usr/bin/python

# (c) 2015 Jose Angel de Bustos Perez <jadebustos@gmail.com>
# Script to execute an ansible playbook (ansible 2.x)

# From the controller machine, where this script is executed, to the nodes
# ssh has to be carried out without password (using rsa keys, by example).

import sys

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager


def main(args):
    # Options definition
    # Custom tuple to store playbook options
    Options = namedtuple('Options', ['connection', 'module_path', 'forks',
                                     'become', 'become_method', 'become_user',
                                     'check'])

    # Object initialization
    variable_manager = VariableManager()
    loader = DataLoader()
    options = Options(connection='ssh',module_path='library',
                      forks=100, become=None, become_method=None,
                      become_user=None, check=False)
    passwords = {}

    # Dinamyc inventory
    inventory = Inventory(loader=loader, variable_manager=variable_manager,
                          host_list=args)

    # Inventory assignation
    variable_manager.set_inventory(inventory)

    # Play creation with tasks
    play_source = dict(
         name="Ansible Play",
         hosts=args,
         gather_facts='no',
         tasks=[
             dict(action=dict(module='shell', args='hostname -f'),
                  register='shell_out'),
             dict(action=dict(module='debug',
                              args=dict(msg='{{shell_out.stdout}}')))
         ]
    )

    play = Play().load(play_source, variable_manager=variable_manager,
                       loader=loader)

    # Running it
    tqm = None
    try:
        tqm = TaskQueueManager(
                      inventory=inventory,
                      variable_manager=variable_manager,
                      loader=loader,
                      options=options,
                      passwords=passwords,
                      stdout_callback='default'
        )
        result = tqm.run(play)
    finally:
        if tqm is not None:
                    tqm.cleanup()

if __name__ == "__main__":
    main(sys.argv)
