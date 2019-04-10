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
from .yaml_parser import find_sources

import oyaml as yaml
import requests
from docopt import docopt
import colorama
from colorama import Fore, Style

debug = False


def main():
    arguments = docopt(__doc__)

    pprint(arguments)
    with open(arguments["YAML"], 'r') as stream:
        try:
            d = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    pprint(d)




    sources, headings = find_sources(d)

    print("Sources")
    print()
    print('\n'.join(sources))
    print()
    print("HEADINGS")
    print()
    print('\n'.join(headings))
    print()



    '''
    config = Config(config_path=arguments["YAML"])

    d = config.data
    print (config)

    print (d)
    '''
if __name__ == '__main__':
    main()
