#!/usr/bin/env python
# pylint: disable=W0621,C0103

"""Example 02: Automatically update system packages

This is only a placeholder to help new participants understand how
remote ssh commands are executed. Like the previous exercise, they will need to
have two things:

  1) The IP address of the machine created (that hasn't had sudo yum update -y)
  2) The key file used to access the machine (with correct permissions).
"""

import os
import sys
import subprocess
import ConfigParser

ANSIBLE_CFG = "./ansible.cfg"

BYPASS_PHRASE = """
        If you want to bypass the configuration, we're only looking for
        the pem file path and the machine address. Then, we'll issue
        this command (which you can do manually):
        ssh -i {pem_file_path} ec2-user@{machine_address}

        But, you may as well do the configuration. As, you'll need it
        for most of the other examples: `cd ..; python configure.py`
"""


def get_private_key_and_hostfile():

    """Read the ansible.cfg file and parse hostfile pathname"""

    if not os.path.exists(ANSIBLE_CFG):
        print """
        The configuration file can't be found. Read the configuration
        instructions in README.md and run `python configure.py`.

        {0}
        """.format(BYPASS_PHRASE)
        sys.exit(1)

    config = ConfigParser.SafeConfigParser()
    config.read('./ansible.cfg')

    hostfile = config.get('defaults', 'hostfile')
    if hostfile is None:
        print "We can't read the hostfile from ansible.cfg"
        sys.exit(2)

    private_key = config.get('defaults', 'private_key_file')

    return (private_key, hostfile)


def get_host(hostfile):
    """Crudely parse hostname from hostfile"""

    if not os.path.exists(hostfile):
        print """
        The hostnames couldn't be read from the webservers
        section of this file '{0}'.

        {1}
        """.format(hostfile, BYPASS_PHRASE)
        sys.exit(3)

    data = None
    with open(hostfile, 'r') as open_hostfile:
        data = open_hostfile.readlines()

    return data[1].strip()


def example_02(pem_file_path, machine_address):
    """An example to show how one executes remote commands via ssh"""

    old_cmd = "ssh -i {pem_file_path} ec2-user@{machine_address}".format(
        pem_file_path=pem_file_path, machine_address=machine_address)
    new_cmd = "{0} -t 'sudo yum update -y'".format(old_cmd)

    print """

    This is the command line you would need to update the operating
    system for this instance:

    {0}

    Press the RETURN to execute the command now
    (and connect to the machine)""".format(new_cmd)
    raw_input('--> ')

    print "\nCommand to execute: {}\n\n".format(new_cmd)

    subprocess.call(new_cmd, shell=True)

    print "\n"

if __name__ == '__main__':
    (private_key, hostfile) = get_private_key_and_hostfile()
    machine_address = get_host(hostfile)
    example_02(private_key, machine_address)
