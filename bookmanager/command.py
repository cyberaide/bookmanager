"""bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager YAML get [--format=FORMAT]
  bookmanager YAML level
  bookmanager YAML epub
  bookmanager YAML download
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

  bookmanager url download YAML [--format=FORMAT]

    downloads the urls into the ./dist directory for local processing

  bookmanager url check YAML [--format=FORMAT]

    checks if the urls in the yaml file exist

  bookmanager url list YAML [--format=FORMAT]

    lists all urls of the yaml file

  bookmanager list YAML [--format=FORMAT]

    lists the yaml file

  Creation of a book:

    1) create a yaml file book.yml
    2) check:    bookmanager url check book.yml
    3) download: bookmanager download check book.yml

    NOt implemented yet the output

    4} epub: bookmanager epub book.yml
    5) html: bookmanager html book.yml
    6) pdf:  bookmanager pdf book.yml

    will be written into the ./dist directory with the names

    book.epup, book.pdf, and the dir html

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
from bookmanager.util import create_section
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
                download(url, path)
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

    def epub(self):

        banner("Creating Epub")

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
        metadata = "./template/epub/metadata.txt"
        options = "--toc --number-sections"
        command = f"pandoc {options} -o ./dist/book.epub --title={title} {files} {metadata}"
        print(command)
        os.system(command)

    def level(self):

        banner("Creating Epub")

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
        book.epub()

    elif arguments["download"]:

       book.download()


    elif arguments.urls:

        book.urls()

    elif arguments.epub:

        book.epub()

    elif arguments.level:

        book.level()


if __name__ == '__main__':
    main()
