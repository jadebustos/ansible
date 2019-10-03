# Ansible modules

This modules can be used in playbooks or python api with ansible runners.

## remote-cmd.py

Ansible module to execute a command in a remote node. The stdout, stderr and return code of the command is returned using a JSON.

This module needs an argument, the command to be executed. If there are blank spaces in the command then quotes have to be used: "command args"
