#!/usr/bin/python

# (c) 2015 Jose Angel de Bustos Perez <jadebustos@gmail.com>
# Script to run an ansible runner using a module (ansible 1.9)

# Ansible module to execute a command and return the stdout, stderr
# and command's return code.

# The module needs one argument, the command to be executed. If there
# are blank spaces then the argument should be "command arguments"

import subprocess
import json
import sys

# Reading arguments from argument file
args_file = sys.argv[1]
args_data = file(args_file).read()


def myexit(stdout, stderr, rc):
    # The output will be printed in stdout using json format
    res = {}
    mystdout = []
    mystderr = []

    mystdout.append(stdout.split('\n'))
    mystderr.append(stderr.split('\n'))

    res['stdout'] = mystdout
    res['stderr'] = mystderr
    res['rc'] = rc

    print json.dumps(res, indent=4)

    sys.exit(0)


def main(args):
    # Executing the command
    cmd = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmdStdout, cmdStderr = cmd.communicate()
    rc = cmd.returncode

    myexit(cmdStdout, cmdStderr, rc)

if __name__ == "__main__":
    main(args_data)
