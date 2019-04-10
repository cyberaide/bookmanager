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

import oyaml as yaml
import requests
from docopt import docopt
import colorama
from colorama import Fore, Style

debug = False

def run(command):
    print(command)
    try:
        output = subprocess.check_output(command,
                                         shell=True,
                                         stderr=subprocess.STDOUT,
                                         )
    except subprocess.CalledProcessError as err:
        print(Fore.red + f"ERROR: {err}")
        sys.exit(1)

    return output.decode('utf-8')


def script(commands, environment):
    for command in commands:
        result = run(command.format(env=environment))
        print(result)


class Git(object):

    @staticmethod
    def url(repo):
        global repos
        if repo in repos['community'] or repo in repos['spring19']:
            return f"https://github.com/cloudmesh-community/{repo}"
        else:
            return f"https://github.com/cloudmesh/{repo}"

    @staticmethod
    def clone(repos):
        for repo in repos:
            print(f"clone -> {repo}", os.path.isdir(Path(f"./{repo}")))

            if not os.path.isdir(Path(f"./{repo}")):
                try:
                    location = Git.url(repo)
                    command = f"git clone {location}.git"
                    r = run(command)
                    print(f"         {r}")
                except Exception as e:
                    print(e)
            else:
                print(Fore.RED + "         ERROR: not downlaoded as repo already exists.")

    @staticmethod
    def status(repos):
        for repo in repos:
            print("status ->", repo)
            os.chdir(repo)
            print(run("git status"))
            os.chdir("../")

    # git clone https://github.com/cloudmesh/get.git

    @staticmethod
    def pull(repos):
        for repo in repos:
            print("pull ->", repo)
            os.chdir(repo)
            print(run("git pull"))
            os.chdir("../")

    @staticmethod
    def install(repos, dev=False):
        for repo in repos:
            print("install ->", repo)
            if dev:
                os.chdir(repo)
                print(run("pip install -e ."))
                os.chdir("../")
            else:
                print(run("pip install {repo}".format(repo=repo)))


# git clone https://github.com/cloudmesh/get.git

def yn_question(msg):
    while True:
        query = input(Fore.RED + msg)
        answer = query.lower().strip()
        if query == '' or answer not in ['yes', 'n']:
            print('Please answer with yes/n!')
        else:
            break
    return answer == 'yes'


def banner(txt, c=Fore.BLUE):
    """prints a banner of the form with a frame of # around the txt::

      ############################
      # txt
      ############################

    :param txt: a text message to be printed
    :type txt: string
    """
    print(c + "#" * 70)
    print(c + f"#{txt}")
    print(c + "#" * 70)



def remove(location):
    print("delete", location)
    try:
        shutil.rmtree(location)
    except Exception as e:
        print(e)


def main():
    arguments = docopt(__doc__)

    pprint(arguments)
    with open(arguments["YAML"], 'r') as stream:
        try:
            d = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    pprint(d)

    import collections


    def process_image(link):
        pass

    def process_program(link):
        pass

    def process_dir(link):
        pass


    def find_sources(d,
                     parent='',
                     sep='/',
                     sources=None,
                     headings=None):

        sources = []
        headings = []

        def _flatten(d, parent='', sep='/'):
            if type(d) == list:
                for entry in d:
                    _flatten(entry, parent=parent)
            elif type(d) == dict:
                key = list(d.keys())[0]
                child = d[key]
                parent = f"{parent}{sep}{key}"
                _flatten(child, parent=parent)
                headings.append(parent)
            else:
                if d.startswith("i "):
                    d=d.replace("i ","")
                    process_image(d)
                elif d.startswith("p "):
                    d=d.replace("p ","")
                    process_program(d)
                elif d.startswith("r "):
                    d=d.replace("r ","")
                    process_dir(d)
                sources.append(f"{parent}/{d}")

        _flatten(d, parent='', sep='/')
        return sources, headings

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
