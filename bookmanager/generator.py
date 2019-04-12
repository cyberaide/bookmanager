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
from bookmanager.config import Config
from cloudmesh.common.FlatDict import FlatDict
from bookmanager.yaml_parser import flatten_json
from cloudmesh.common.util import readfile, writefile
from bookmanager.util import readyaml
import oyaml as yaml
import requests
from docopt import docopt
import colorama
from colorama import Fore, Style
from cloudmesh.common.dotdict import dotdict
from cloudmesh.DEBUG import VERBOSE
debug = False


def main():
    arguments = dotdict(docopt(__doc__))

    VERBOSE(arguments)

    config = Config(config=arguments.YAML)

    VERBOSE(config.book)
    VERBOSE(config.variables)

    print()
    pprint(flatten_json(config.book, output="{parent}/{key}"))
    print()
    pprint(flatten_json(config.book, output="{counter} {parent}/{key}"))
    print()
    pprint(flatten_json(config.book, output="- [ ] {parent}/{key}"))
    print()

    '''
    print (config)

    print (d)
    '''


if __name__ == '__main__':
    main()
