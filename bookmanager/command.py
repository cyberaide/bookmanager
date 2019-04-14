"""bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager YAML cover
  bookmanager YAML get [--format=FORMAT] [--force]
  bookmanager YAML download
  bookmanager YAML level
  bookmanager YAML epub [--force]
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
    available for test purposes.

    You can create an epub with

      bookmanager YAML get [--format=FORMAT]

    The command seatches for all images within the markdown documet and fetches
    them so the document can be created locally with the images. We assume all
    images in the md document are for now not specified via http locations but
    via relative locations.

    To view the document use your favourite ePub Reader

    Other commands include:

      bookmanager YAML download [--format=FORMAT]

        downloads the urls into the ./dest directory for local processing

      bookmanager YAML check [--format=FORMAT]

        checks if the urls in the yaml file exist

      bookmanager YAML urls  [--format=FORMAT]

        lists all urls of the yaml file

      bookmanager YAML list [--format=FORMAT]

        lists the yaml file


    Not implemented are the following features:

    1) pdf:  bookmanager pdf book.yml

    YAML Table of Contents format:

      The table of contents for the book can be controled with a simple yaml
      file that has some specific contectual enhancements. THis include the
      creation of a BOOK section that has the sections outlined in hierarchical
      form, and contains chapter and section headers without links that are
      automatically generated.

    Here is an example of a simple TOC yaml file:

    * https://github.com/cyberaide/bookmanager/blob/master/tests/python.yml

    Bugs and enhancement suggestions:

    * https://github.com/cyberaide/bookmanager/issues

"""
import os
import sys
from pathlib import Path
from pprint import pprint

import requests
from bookmanager.config import Config
from bookmanager.cover import Cover
from bookmanager.util import create_metadata, create_css
from bookmanager.util import create_section
from bookmanager.util import download as page_download
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.util import banner, path_expand
from docopt import docopt
from tabulate import tabulate

debug = False


class Book:

    def __init__(self, arguments):

        self.config = Config(config=arguments.YAML)
        self.metadata = self.config["metadata"]
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
                    print(" -> ok")
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
                print('...', end=' ')
                # pprint (entry)
                url = entry["url"]
                path = entry["path"]
                path = f"./dest/book{path}"
                page_download(url, path, entry['level'])
                print()
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

        print(result)

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
                    "./dest/book{path}/{basename}".format(**entry))

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

        # metadata["stylesheet"] = path_expand(metadata["stylesheet"])
        title = self.metadata["title"]

        if output == "epub":

            result = \
                self.config.flatten(
                    book=title,
                    title=title,
                    section="{topic}",
                    header="{topic}",
                    indent=""
                )

            dirs = []
            for section in result:
                if section["kind"] == "section":
                    # pprint(section)
                    path = section["path"]
                    dirs.append(path_expand(f"./dest/book{path}"))
            dirs = set(dirs)
            # dirs = find_image_dirs(directory='./dest')

            create_metadata(self.metadata, "./dest/book/metadata.txt")
            create_css(self.metadata, "./dest/book/epub.css")

            # pprint(self.metadata)

            directories = (":".join(dirs))
            metadata = path_expand("./dest/book/metadata.txt")
            filename = self.metadata["filename"]

            options = "--toc --number-sections"
            resources = f"--resource-path={directories}"
            epub = path_expand(f"./dest/{filename}")
            # noinspection PyPep8
            command = f'cd dest/book; pandoc {options} {resources} -o {epub} {files} {metadata}'
            # pprint(command.split(" "))

        elif output == "pdf":
            metadata = "./dest/metadata.txt"
            options = "--toc --number-sections"
            command = f'pandoc {options} -o ./dest/book.pdf {files}'

        elif output == "html":
            metadata = "./dest/metadata.txt"
            options = "--toc --number-sections"
            command = f'pandoc {options} -o ./dest/book.html {files}'

        elif output == "docx":
            metadata = "./dest/metadata.txt"
            options = "--toc --number-sections"
            command = f'pandoc {options} -o ./dest/book.docx {files}'

        else:
            raise ValueError("this output format is not yet supported")

        VERBOSE(command)
        os.system(command)

    def level(self):

        banner("Creating Level")

        title = self.metadata["title"]

        result = \
            self.config.flatten(
                book=title,
                title="title",
                section="{topic}",
                header="{topic}",
                indent=""
            )
        os.system("echo > log.txt")
        for entry in result:
            if entry["kind"] == "section":
                entry["local"] = path_expand(
                    "./dest/book{path}/{basename}".format(**entry))

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
                # noinspection PyPep8
                command = "pandoc --base-header-level={level} -o ./dest/tmp.md {local} > log.txt".format(
                    **entry)
                # print(command)
                print("convert", end=' ')
                sys.stdout.flush()
                os.system(command)
                command = "cp ./dest/tmp.md {local} > log.txt".format(**entry)
                # print(command)
                os.system(command)
                os.system("rm -f ./dest/tmp.md")
                os.system("rm -f log.txt")

                print('...', end=' ')
                sys.stdout.flush()
                print()

    def cover(self):

        cover = Cover()

        metadata = dotdict(self.config["metadata"])

        pprint(metadata)
        image = metadata.image
        dest = metadata.dest

        image = path_expand(f"./{dest}/{image}")
        Path(os.path.dirname(image)).mkdir(parents=True, exist_ok=True)

        banner(f"Generating Cover Page: {image}")

        table = []
        for k, v in metadata.items():
            table.append([k, v])
        print(tabulate(table, tablefmt="grid",
                       headers=["Attrbute", "Value"]))

        cover.generate(
            image=image,
            background=metadata.background,
            title=metadata.title,
            subtitle=metadata.subtitle,
            author=metadata.author,
            email=metadata.email,
            webpage=metadata.url
        )


def main():
    arguments = dotdict(docopt(__doc__))
    arguments["FORMAT"] = arguments["--format"]

    # pprint(arguments)

    book = Book(arguments)

    if arguments.force:
        os.system("rm -rf dest/book/epub.css")
        os.system("rm -rf dest/book/cover.png")
        os.system("rm -rf dest/bool/metadata.txt")

    if arguments.cover:

        book.cover()

    elif arguments.info:

        # pprint(config.book)
        # pprint(config.variables)

        raise NotImplementedError

    elif arguments.list and (arguments.FORMAT in ["md", "markdown"]):

        book.list("markdown")

    elif arguments.list and (arguments.FORMAT in ["list"]):

        book.list("list")

    elif arguments.url and arguments.check:

        book.check()

    elif arguments["get"]:

        book.cover()
        book.download()
        book.level()
        book.generate("epub")

    elif arguments["download"]:

        book.download()

    elif arguments.urls:

        book.urls()

    elif arguments.epub:

        book.cover()
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
