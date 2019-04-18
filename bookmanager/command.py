"""bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager version
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
  bookmanager YAML list [--format=FORMAT] [--details]


Arguments:
  YAML   the yaml file

Options:
  -h --help
  -f, --format=FORMAT     [default: markdown]
  -d, --details           [default: False]

Description:

    In principal you only need one command at this time. All other commands are
    available for test purposes.

    You can create an epub with

      bookmanager YAML get [--format=FORMAT]

    The command searches for all images within the markdown document and fetches
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

      The table of contents for the book can be controlled with a simple yaml
      file that has some specific contextual enhancements. THis include the
      creation of a BOOK section that has the sections outlined in hierarchical
      form, and contains chapter and section headers without links that are
      automatically generated.

    Here is an example of a simple TOC yaml file:

    * https://github.com/cyberaide/bookmanager/blob/master/tests/python.yml

    Bugs and enhancement suggestions:

    * https://github.com/cyberaide/bookmanager/issues

"""
import os

from cloudmesh.common.dotdict import dotdict
from docopt import docopt
from bookmanager.book import Book
from bookmanager.__version__ import version
import sys

debug = False


def main():
    arguments = dotdict(docopt(__doc__))
    arguments["FORMAT"] = arguments["--format"]
    force = arguments["--force"]
    # pprint(arguments)

    if arguments.version:
        print(version)
        sys.exit(0)

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

        details = arguments["--details"]
        book.list("markdown", details)

    elif arguments.list and (arguments.FORMAT in ["list"]):

        book.list("list")

    elif arguments.check:

        book.check()

    elif arguments["get"]:

        book.cover()
        book.download(force)
        book.level()
        book.generate("epub")

    elif arguments["download"]:

        book.download(force)

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
