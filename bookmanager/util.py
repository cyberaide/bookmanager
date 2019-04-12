import subprocess
import oyaml as yaml
import colorama
from colorama import Fore, Style
import sys
import shutil


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
