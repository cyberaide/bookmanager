import os
from pathlib import Path
from colorama import Fore
from bookmanager.run import run


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
                # noinspection PyPep8
                print(
                    Fore.RED + "         ERROR: not downlaoded as repo already exists.")

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
