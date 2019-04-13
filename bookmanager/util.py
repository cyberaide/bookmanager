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
from pprint import pprint
import pkg_resources
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import writefile,readfile

def create_section(filename, header):
    writefile(filename, f"# {header}\n\n")

def git_download(repo, path, destination):
    os.system(f"svn export https://github.com/{repo}/trunk/{path} {destination}")


import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension

from shutil import copyfile

import sys
import glob
import os


def create_metadata(metadata, location):
    location = path_expand(location)
    Path(os.path.dirname(location)).mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(location):
        metadata_file = pkg_resources.resource_filename("bookmanager",
                                              'template/epub/metadata.txt')

        content = readfile(metadata_file)
        content = content.format(**metadata)
        writefile(location, content)


def create_css(metadata, location):
    location = path_expand(location)
    Path(os.path.dirname(location)).mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(location):
        css_file = pkg_resources.resource_filename("bookmanager",
                                                        'template/epub/epub.css')

        copyfile(css_file, location)



def find_image_dirs(directory='dest'):
    directory = path_expand(directory)
    directories = []

    p = Path(directory)
    images = []
    for t in ['png', "PNG", "JPG", "jpg", "JPEG", "jpeg"]:
        images = images + list(p.glob(f"**/*{t}"))
    dirs = []
    for image in images:
        dirs.append(os.path.dirname(image))
    dirs = set(dirs)
    return dirs

# First create the treeprocessor

class ImgExtractor(Treeprocessor):
    def run(self, doc):
        "Find all images and append to markdown.images. "
        self.markdown.images = []
        for image in doc.findall('.//img'):
            self.markdown.images.append(image.get('src'))

# Then tell markdown about it

class ImgExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        img_ext = ImgExtractor(md)
        md.treeprocessors.add('imgext', img_ext, '>inline')

# Finally create an instance of the Markdown class with the new extension

def find_images(content):
    md = markdown.Markdown(extensions=[ImgExtExtension()])
    html = md.convert(content)
    return md.images


def get_file_from_git(url, directory, filename):
    d = Path(directory)
    d.mkdir(parents=True, exist_ok=True)
    d.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, allow_redirects=True)

    output = Path(directory) / filename
    with open(output, 'wb') as f:
        f.write(r.content)
    return r

def download(url, name, level=0):
    name = path_expand(name)
    basename = os.path.basename(name)
    directory = name # os.path.dirname(name)
    filename = Path(directory) / os.path.basename(url)

    r = get_file_from_git(url, directory, filename)

    if b"![" in r.content:
        images = find_images(r.content)
        print()
        print()
        print('   ' * (level+2), "Downloading", len(images), " images")

        dirurl = os.path.dirname(url)
        for image in images:
            print ('   ' * (level+2), "Download", image, end=" ")
            image_name = os.path.basename(image)
            image_url = f"{dirurl}/{image}"

            destination =  f"{directory}"
            image_dir = os.path.dirname(f"{destination}/{image}")

            d = Path(image_dir)
            d.mkdir(parents=True, exist_ok=True)
            r = get_file_from_git(image_url, image_dir, image_name)
            print()

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
