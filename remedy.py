#!/usr/bin/env python
"""remedy.py Check and update bash using yum or apt-get.

Usage:
  remedy.py <IP_LIST>

Options:
  -h --help     Show this screen.
  -V --version  Show vers
"""

import re
import sys

from fabric.api import env
from termcolor import colored
from getpass import getpass
from docopt import docopt

from lib.remedy import cure

arg = docopt(__doc__, version="REMEDY 0.0")

# Main
try:
    m = re.compile("(\d{1,3}\.){3}\d{1,3}")

    with open(arg["<IP_LIST>"]) as fp_hosts:
        sys.stderr.write("User: ")
        env.user = raw_input()
        env.password = getpass("Password: ")

        print(colored("Failed IPs: ", "red", attrs=['bold']))
        for host in fp_hosts:
            host = host.strip()

            if len(host) == 0:
                continue # accept empty line

            if not m.match(host):
                print("Possibly bad IP ? `%s`" % host)
                continue

            result = cure(host)
            if result[0] < 0 :
                print("%s \t\t# %s" % (host, colored(result[1], 'red', attrs=['bold'])))

except KeyboardInterrupt:
    print(colored("Aborted", "cyan", attrs=['bold']))
except IOError:
    print(colored("Can't open file `%s`, aborted" % arg["<IP_LIST>"], "red", attrs=['bold']))

