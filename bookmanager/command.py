"""bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager YAML get [--format=FORMAT]
  bookmanager YAML download
  bookmanager YAML level
  bookmanager YAML epub
  bookmanager YAML pdf
  bookmanager YAML html
  bookmanager YAML docx
  bookmanager YAML check [--format=FORMAT]
  bookmanager YAML urls [--format=FORMAT]
  bookmanager YAML list [--format=FORMAT]
  bookmanager info


Arguments:
  YAML   the yaml file

Options:
  -h --help
  -f, --format=FORMAT     [default: markdown]

Description:

    In principal you only need one command at this time. All other commands are
    available for test purpuses.

    You can create an epub with

      bookmanager YAML get [--format=FORMAT]


    Other commands include:

      bookmanager YAML download [--format=FORMAT]

        downloads the urls into the ./dist directory for local processing

      bookmanager YAML check [--format=FORMAT]

        checks if the urls in the yaml file exist

      bookmanager YAML urls  [--format=FORMAT]

        lists all urls of the yaml file

      bookmanager YAML list [--format=FORMAT]

        lists the yaml file

    Not implemented are the following features:

    1) html: bookmanager html book.yml
    2) pdf:  bookmanager pdf book.yml

    will be written into the ./dist directory with the names

    book.epub, book.pdf, and the dir html

  YAML Table of Contents format

    The table of contents for the book can be controled with a simple yaml file
    that has some specific contectual enhancements. THis include the creation of
    a BOOK section that has the sections outlined in hierarchical form, and
    contains chapter and section headers without links that are automatically
    generated.

    Here is an example of a simple TOC yaml file:

    * <https://github.com/cyberaide/bookmanager/blob/master/tests/python.yml>


"""
from bookmanager.config import Config
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.common.util import banner, path_expand
from cloudmesh.shell.command import map_parameters
from cloudmesh.common.dotdict import dotdict
from docopt import docopt
from pprint import pprint
from bookmanager.util import download
import os
from bookmanager.util import create_section, find_image_dirs
import sys

import requests

debug = False

class Book:

    def __init__(self, arguments):

        self.config = Config(config=arguments.YAML)
        self.arguments = arguments

    def list(self, output):
        banner("list")

        banner("MARDOWN")

        if output == "markdown":

            result = \
                self.config.flatten(
                    book="My Book",
                    title="- {book}",
                    section="{indent}- [ ] {counter} [{topic}]({url}) {level}",
                    header="{indent}- [ ] {counter} {topic} {level}",
                    indent="  "
                )

            print(self.config.output(result, kind="text"))


        else:

            banner("list")

            banner("LITS LIST")

            result = \
                self.config.flatten(
                    book="My Book",
                    title="- {book}",
                    section="{indent}- [ ] [{topic}]({url}) {level}",
                    header="{indent}- [ ] {topic} {level}",
                    indent="  "
                )

            print(self.config.output(result, kind="list"))

    def check(self):

        banner("check")

        result = \
            self.config.flatten(
                book="",
                title="",
                section="{url}",
                header="",
                indent=""
            )

        for entry in result:
            url = entry["url"]
            if url.startswith("http"):
                print(url, end="")
                response = requests.get(url)
                if response.status_code < 400:
                    print (" -> ok")
                else:
                    print("error", response.status_code)

    def download(self):

        banner("get")

        result = \
            self.config.flatten(
                book="My Book",
                title="{book}",
                section="{topic}",
                header="{topic}",
                indent=""
            )

        for entry in result:
            if entry["kind"] == "section":
                print(entry["level"] * "   ", entry["counter"], entry["name"],
                      end=' ')
                print('download', end=' ')
                # pprint (entry)
                url = entry["url"]
                path = entry["path"]
                path = f"./dist{path}"
                download(url, path, entry['level'])
                print("ok")
            elif entry["kind"] == 'header':
                print(entry['level'] * "   ", entry['counter'], entry['topic'])


    def urls(self):

        banner("URL")

        if self.arguments.FORMAT in ["md", "markdown"]:
            kind = "text"
        else:
            kind = "list"


        result = \
            self.config.flatten(
                book="",
                title="",
                section="{url}",
                header="",
                indent=""
            )

        print (result)

        print('\n'.join(self.config.output(result, kind="url")))

    def generate(self, output):

        banner(f"Creating {output}")

        result = \
            self.config.flatten(
                book="",
                title="",
                section="{url}",
                header="",
                indent=""
            )

        files = []
        for entry in result:
            if entry["kind"] == "section":
                entry["local"] = path_expand(
                    "./dist{path}/{basename}".format(**entry))

            if entry["kind"] == "header":
                entry["local"] = path_expand(
                    "./{path}/{basename}.md".format(**entry))

            if entry["kind"] in ["section", "header"]:
                url = entry["url"]
                path = entry["path"]
                basename = entry["basename"]
                local = entry["local"]
                files.append(local)

        banner("Finding Contents")

        print("Number of included Sections:", len(result))

        banner("Creating Command")


        files = " ".join(files)
        title = "Example"
        if output == "epub":

            result = \
                self.config.flatten(
                    book="My Book",
                    title="{book}",
                    section="{topic}",
                    header="{topic}",
                    indent=""
                )

            dirs = []
            for section in result:
                if section["kind"] == "section":
                    pprint(section)
                    path = section["path"]
                    dirs.append(path_expand(f"./dist{path}"))
            dirs = set(dirs)
            # dirs = find_image_dirs(directory='./dist')

            directories = (":".join(dirs))
            metadata = "./template/epub/metadata.txt"
            options = "--toc --number-sections"
            resources = f"--resource-path={directories}"
            command = f"pandoc {options} {resources} -o ./dist/book.epub --title={title} {files} {metadata}"


        elif output == "pdf":
            metadata = "./template/epub/metadata.txt"
            options = "--toc --number-sections"
            command = f"pandoc {options} -o ./dist/book.pdf --title={title} {files}"

        elif output == "html":
            metadata = "./template/epub/metadata.txt"
            options = "--toc --number-sections"
            command = f"pandoc {options} -o ./dist/book.html --title={title} {files}"

        elif output == "docx":
            metadata = "./template/epub/metadata.txt"
            options = "--toc --number-sections"
            command = f"pandoc {options} -o ./dist/book.docx --title={title} {files}"

        else:
            raise ValueError("this output format is not yet supported")

        print(command)
        os.system(command)

    def level(self):

        banner("Creating Level")

        result = \
            self.config.flatten(
                book="My Book",
                title="{book}",
                section="{topic}",
                header="{topic}",
                indent=""
            )
        os.system("echo > log.txt")
        for entry in result:
            if entry["kind"] == "section":
                entry["local"] = path_expand(
                    "./dist{path}/{basename}".format(**entry))

            if entry["kind"] == "header":
                entry["local"] = path_expand(
                    "./{path}/{basename}.md".format(**entry))
                create_section(entry["local"], entry["name"])

            if entry["kind"] in ["header", "section"]:
                entry["level"] = entry["level"] - 1
                print(entry["level"] * "   ", entry["counter"], entry["name"],
                      end=' ')
                sys.stdout.flush()
                # pprint(entry)
                command = "pandoc --base-header-level={level} -o ./dist/tmp.md {local} > log.txt".format(
                    **entry)
                # print(command)
                print("convert", end=' ')
                sys.stdout.flush()
                os.system(command)
                command = "cp ./dist/tmp.md {local} > log.txt".format(**entry)
                # print(command)
                os.system(command)
                print('ok', end=' ')
                sys.stdout.flush()
                print()


def main():
    arguments = dotdict(docopt(__doc__))
    arguments["FORMAT"] = arguments["--format"]

    pprint(arguments)

    book = Book(arguments)


    if arguments.info:

        #pprint(config.book)
        #pprint(config.variables)

        raise NotImplementedError

    elif arguments.list and (arguments.FORMAT in ["md", "markdown"]):

        book.list("markdown")

    elif arguments.list and (arguments.FORMAT in ["list"]):

        book.list("list")

    elif arguments.url and arguments.check:

        book.check()

    elif arguments["get"]:

        book.download()
        book.level()
        book.generate("epub")

    elif arguments["download"]:

       book.download()


    elif arguments.urls:

        book.urls()

    elif arguments.epub:

        book.generate("epub")

    elif arguments.pdf:

        book.generate("pdf")

    elif arguments.html:

        book.generate("html")

    elif arguments.docx:

        book.generate("docx")

    elif arguments.level:

        book.level()


if __name__ == '__main__':
    main()
