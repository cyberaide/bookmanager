import subprocess
import oyaml as yaml
import colorama
from colorama import Fore, Style
import sys
import shutil
import requests
import os
from pathlib import Path
import pathlib

from cloudmesh.common.util import path_expand
from cloudmesh.common.util import writefile

def create_section(filename, header):
    writefile(filename, f"# {header}\n\n")


def download(url, name):
    name = path_expand(name)
    basename = os.path.basename(name)
    directory = name # os.path.dirname(name)
    filename = Path(directory) / os.path.basename(url)

    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, allow_redirects=True)

    output = Path(directory) / filename
    with open(output, 'wb') as f:
        f.write(r.content)

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


def readyaml(name):
    with open(name, 'r') as stream:
        try:
            d = yaml.safe_load(stream)
            return d
        except yaml.YAMLError as exc:
            print(exc)
    return []
