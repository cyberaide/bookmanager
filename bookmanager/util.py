import os
import shutil
import subprocess
import sys
from pathlib import Path
from shutil import copyfile

import markdown
import oyaml as yaml
import pkg_resources
import requests
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import writefile, readfile
from colorama import Fore
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


def create_section(filename, header, n):
    writefile(filename, ("#" * n) + f" {header}\n\n")


def git_download(repo, path, destination):
    os.system(
        f"svn export https://github.com/{repo}/trunk/{path} {destination}")


def create_metadata(metadata, location):
    location = path_expand(location)
    Path(os.path.dirname(location)).mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(location):
        metadata_file = pkg_resources.resource_filename(
            "bookmanager",
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
        """Find all images and append to markdown.images. """
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


def find_smalest_headers(content):
    """
    find the smalest header level
    :param content:
    :type content:
    :return:
    :rtype:
    """
    ignore = False
    lines = content.split("\n")
    headers = []
    for line in lines:
        if line.startswith("`"):
            ignore = not ignore
            break
        if line.startswith("#") and not ignore:
            headers.append(line.split(" ")[0])
    headers = set(headers)
    level = sorted(headers, key=len)
    if len(level) == 0:
        level = 1
    else:
        level = len(level[0])
    return level


def reduce_headers(content, level, indent=1):
    """
    replaces the #* with level number of #
    :param content:
    :type content:
    :param level:
    :type level:
    :return:
    :rtype:
    """
    ignore = False
    lines = content.split("\n")
    headers = []
    out = []
    for line in lines:
        if line.startswith("`"):
            ignore = not ignore

        if line.startswith("#") and not ignore:
            line = line.replace("#" * level, "#")
            line = line.replace("# ", "#" * (indent - 1) + " ")

        out.append(line)
    return out


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
    directory = name  # os.path.dirname(name)
    filename = Path(directory) / os.path.basename(url)

    if os.path.exists(filename):
        print(Fore.RED + "Warning: file alredy exists" + Fore.RESET, end="")
        return

    r = get_file_from_git(url, directory, filename)

    if b"![" in r.content:
        images = find_images(r.content)

        # from pprint import pprint ; pprint(images)
        print()
        print()
        print('   ' * (level + 2), "Downloading", len(images), " images")

        dirurl = os.path.dirname(url)
        for image in images:
            if not image.startswith("http"):
                print('   ' * (level + 2), "Download", image, end=" ")
                image_name = os.path.basename(image)
                image_url = f"{dirurl}/{image}"

                destination = f"{directory}"
                image_dir = os.path.dirname(f"{destination}/{image}")

                d = Path(image_dir)
                d.mkdir(parents=True, exist_ok=True)

                r = get_file_from_git(image_url, image_dir, image_name)
                print("...")
            else:
                print('   ' * (level + 2), "Skipping", image)


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
    :param c: a char used for the frame
    :type c: char
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
