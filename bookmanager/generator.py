"""bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager list [YAML]


Arguments:
  YAML   the yaml file

Options:
  -h --help

Description:

    TBD

"""
import os
import re
import shutil
import subprocess
import sys
import textwrap
import webbrowser
from pathlib import Path
from pprint import pprint
from tabulate import tabulate
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.FlatDict import FlatDict
from bookmanager.yaml_parser import flatten_json
from cloudmesh.common.util import readfile

import oyaml as yaml
import requests
from docopt import docopt
import colorama
from colorama import Fore, Style

debug = False

def read_yaml(name):
    with open(name, 'r') as stream:
        try:
            d = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return d

def main():
    arguments = docopt(__doc__)

    pprint(arguments)

    d = read_yaml(arguments["YAML"])
    pprint(d)

    pprint(flatten_json(d, output="{parent}/{key}"))
    pprint(flatten_json(d, output="{counter} {parent}/{key}"))
    pprint(flatten_json(d, output="- [ ] {parent}/{key}"))

    r = readfile(arguments["YAML"])
    print(r)
    '''
    config = Config(config_path=arguments["YAML"])

    d = config.data
    print (config)

    print (d)
    '''
if __name__ == '__main__':
    main()
