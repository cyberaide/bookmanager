import os
import shutil
import subprocess
import sys
from pathlib import Path
from shutil import copyfile
import datetime

import markdown
import oyaml as yaml
import pkg_resources
import requests
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import writefile, readfile
from colorama import Fore
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from pprint import pprint
import copy
from collections import Counter
from cloudmesh.git.Git import Git


def git_raw_url(url: str, branch="main"):
    """
    Converts the url into a raw url and returns a list of
    repo, branch, name, raw

    example urls are:

    raw = "https://raw.githubusercontent.com/cybertraining-dsc/reu2022/main/project/rivanna.md"
    url = "https://github.com/cybertraining-dsc/reu2022/blob/main/project/rivanna.md"
    blob = "https://github.com/cybertraining-dsc/reu2022/blob/main/project/rivanna.md"
    print (git_raw_url(url))
    print (git_raw_url(raw))

    Args:
        url (str): teh URL
        branch (str): The name of the branch, default main

    Returns:

    """

    if url.startswith("https://github.com/"):
        _url = url.replace("https://github.com/", "")
        repo, rest = _url.split("/blob/", 1)
        print (repo, rest)
        branch, name = rest.split("/", 1)
        raw = f"https://raw.githubusercontent.com/{repo}/{branch}/{name}"
        blob = f"https://github.com/{repo}/blob/{branch}/{name}"
    elif url.startswith('https://raw.githubusercontent.com/'):
        _url = url.replace("https://raw.githubusercontent.com/", "")

        repo, name = _url.split(f"/{branch}/", 1)
        raw = f"https://raw.githubusercontent.com/{repo}/{branch}/{name}"
        blob = f"https://github.com/{repo}/blob/{branch}/{name}"
    elif url.startswith("file:"):
        repo = Git.repo(url)
        blob = Git.blob(url)
        name = Git.name(url)
        root = Git.root(url)
        branch = Git.branch(url)
        filename = Git.filename(url)
        raw = f"https://raw.githubusercontent.com/{name}/{branch}/{filename}"

    else:
        repo = None
        branch = None
        name = None
        blob = url
        raw = url

    return repo, branch, name, raw, blob

def filewrap(path, prefix, postfix):
    content = readfile(path)
    if not content.startswith(prefix):
        content = prefix + "\n" + content
    if not content.endswith(postfix):
        content = content + "\n" + postfix

def find_unique_name(entry, entries):
    locations = []
    for element in entries:
        if element.kind == "section":
            # print (entry)
            locations.append(element.destination)

    counts = Counter(locations)

    duplicates = {k: v for k, v in counts.items() if v > 1}

    if entry.destination in duplicates:
        base, ending = entry.destination.rsplit(".", 1)
        counter = entry.counter
        entry.destination = str(Path(f"{base}-{counter}.{ending}"))
    return entry.destination

def cat_bibfiles(directory, output):
    d = path_expand(directory)
    bibs = list(Path(d).glob("**/*.bib"))

    pprint(bibs)

    r = ""
    for bib in bibs:
        bib = str(bib)
        content = readfile(bib)
        r = r + "\n\n% " + bib + "\n\n" + content
    writefile(output, r)

    return list(bibs)


def create_section(filename, header, n):
    if "{" in header:
        prefix, rest = header.split("{", 1)
        header = prefix.replace("_", " ") + "{" + rest
    else:
        header = header.replace("_", " ")
    writefile(filename, ("#" * n) + f" {header}\n\n")


def git_download(repo, path, destination):
    try:
        os.system(
            f"svn export https://github.com/{repo}/trunk/{path} {destination}")
    except:
        print("ERROR: file not found", repo, path)

def create_metadata(metadata, location, kind="epub"):

    location = path_expand(location)
    Path(os.path.dirname(location)).mkdir(parents=True, exist_ok=True)
    metadata_file = pkg_resources.resource_filename(
        "bookmanager",
        f'template/{kind}/metadata.txt')

    meta = copy.deepcopy(metadata)
    if "date" not in meta:
        meta["date"] = str(datetime.datetime.now())

    for field in ["author", "title"]:
        meta[field] = meta[field].replace("\n", " ")

    content = readfile(metadata_file)

    content = content.format(**meta)
    writefile(location, content)
    os.system("sync")

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


def find_smallest_headers(content):
    """
    find the smallest header level
    :param content:
    :type content:
    :return:
    :rtype:
    """
    ignore = False
    lines = content.splitlines()
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
    :param indent:
    :type indent:
    :return:
    :rtype:
    """
    ignore = False
    lines = content.splitlines()
    headers = []
    out = []
    for line in lines:
        if line.startswith("`"):
            ignore = not ignore

        if line.startswith("#") and not ignore:
            line = line.replace("#" * level, "#")
            line = line.replace("# ", "#" * (indent - 1) + " ")
            # if "_" in line:
            #    line = line.replace("_", " ")

        out.append(line)
    return out


def get_file_from_git(url, directory, filename):
    d = Path(directory)
    d.mkdir(parents=True, exist_ok=True)

    if url.startswith("/"):
        try:
            copyfile(url, Path(f"{directory}/{filename}"))
        except FileNotFoundError:
            print(f"\n\nERROR:\n{directory}/{filename} could not be found\n\n")
            sys.exit()
        r = ""
    else:

        repo, branch, name, raw, blob = git_raw_url(url)

        r = requests.get(raw, allow_redirects=True, headers={'Cache-Control': 'no-cache'})

        if r.status_code == 200:
            output = Path(directory) / filename
            with open(output, 'wb') as f:
                # if url.endswith(".bib"):
                #    VERBOSE(url)
                #    VERBOSE(output)
                #    VERBOSE(r.content)
                #    f.write(b"% " + url.encode('ascii') + "\n" +
                #            b"% " + output.encode('ascii') + "\n" +
                #            r.content)
                #    f.write("%" + url + "\n" + r.content)
                # else:
                f.write(r.content)
        else:
            if not url.endswith(".bib"):
                print()
                print("can not find")
                print()
                print(url)
                print("   ", directory, filename)
    return r


class Result(object):
    def __init__(self):
        self.content = None
        self.status_code = None


def add_link_to_file(url, filename, variables):
    lines = readfile(Path(f"{filename}"))
    lines = lines.splitlines()
    if len(lines) == 0:
        lines.append("\n")

    repo, branch, name, raw, link = git_raw_url(url)

    if "{" in lines[0]:
        headline, ref = lines[0].split("{", 1)
        lines[0] = headline + f" [:cloud:]({link}) " + "{" + ref
    else:
        lines[0] = lines[0] + f" [:cloud:]({link})"


    #lines[0] = lines[0].replace("raw.githubusercontent.com", "github.com")
    ##lines[0] = lines[0].replace("/master/", "/master/master/")
    #lines[0] = lines[0].replace("/master/", "/blob/master/")

    if 'file.base' in variables and "file.github" in variables:
        path = str(Path(variables["file.base"]).resolve())
        lines[0] = lines[0].replace(path, variables["file.github"])

    lines = '\n'.join(lines)
    writefile(filename, lines)


def get_file_from_local(url, directory, filename):
    d = Path(directory)
    d.mkdir(parents=True, exist_ok=True)

    output = Path(directory) / filename

    source = Path(url.replace("file:", "")).resolve()

    copyfile(source, output)

    r = Result()
    r.content = readfile(output).encode()
    r.status_code = "200"
    return r


def download(url, destination, level=0, force=False, spec=None):
    destination = str(Path(destination).resolve())

    basename = os.path.basename(destination)
    directory = os.path.dirname(destination)

    filename = destination

    if os.path.exists(filename) and not force:
        print(Fore.RED + "Warning: file already exists" + Fore.RESET, end="")
        return

    content = ""
    if url.startswith("http"):
        r = get_file_from_git(url, directory, filename)
    elif url.startswith("file"):
        r = get_file_from_local(url, directory, filename)
    elif url.startswith("/"):
        r = get_file_from_local(url, directory, filename)
    else:
        print("prefix in url not supported", url)
        sys.exit(1)

    content = r.content

    #
    # DOWNLOAD IMAGES
    #
    # if type(content) == str:
    #    image_found = "![" in content
    #
    # else:

    image_found = b"![" in content

    if image_found:
        images = find_images(content)

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

    #
    # DOWNLOAD BIB from guessed bibfile
    #

    try:

        content = ""
        if url.startswith("http"):
            r = get_file_from_git(url, directory, filename)
        elif url.startswith("file:"):
            r = get_file_from_local(url, directory, filename)
        elif url.startswith("/"):
            r = get_file_from_local(url, directory, filename)
        else:
            print("prefix in url not supported", url)
            sys.exit(1)

        if url.startswith("http"):
            bib_url_guess = str(url).split(".md")[0] + ".bib"
            bib_filename_guess = str(filename).split(".md")[0] + ".bib"

            check = get_file_from_git(bib_url_guess,
                                      directory,
                                      bib_filename_guess)

        elif url.startswith("file:"):

            bib_url_guess = str(url).split(".md")[0] + ".bib"
            bib_filename_guess = str(filename).split(".md")[0] + ".bib"

            check = get_file_from_local(url, directory, filename)
        elif url.startswith("/"):

            bib_url_guess = str(url).split(".md")[0] + ".bib"
            bib_filename_guess = str(filename).split(".md")[0] + ".bib"

            check = get_file_from_local(url, directory, filename)
        else:
            print("H")
            print("prefix in url not supported", url)
            sys.exit(1)

        if check.status_code == 200:
            print('   ' * (level + 2), "Download",
                  os.path.basename(bib_filename_guess))
    except Exception as e:
        print(e)

    add_link_to_file(url, filename, spec)



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
