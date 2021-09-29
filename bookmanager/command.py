"""bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager version
  bookmanager YAML cover
  bookmanager YAML get [--format=FORMAT] [--force]
  bookmanager YAML download
  bookmanager YAML level
  bookmanager YAML epub [--force]
  bookmanager YAML pdf [--force]
  bookmanager YAML html
  bookmanager YAML md
  bookmanager YAML tex
  bookmanager YAML docx
  bookmanager YAML check [--format=FORMAT]
  bookmanager YAML urls [--format=FORMAT]
  bookmanager YAML list [--format=FORMAT] [--details]
  bookmanager YAML pdfget [--force]

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

        The command searches for all documents within the markdown document and
        fetches them so the document can be created locally. We assume all
        images in the md document are for now not specified via http locations
        but via relative locations. E.g. the images must be in an images folder
        next to the document.

        To view the document use your favourite ePub Reader

    Other commands include:

      bookmanager YAML download [--format=FORMAT]

        downloads the urls into the ./dest directory for local processing

      bookmanager YAML check [--format=FORMAT]

        checks if the urls in the yaml file exist

      bookmanager YAML urls  [--format=FORMAT]

        lists all urls of the yaml file

      bookmanager YAML list [--format=FORMAT] [--details]

        lists the yaml file

        If you specify as format list, you get presented with a list of dicts
        that can be used for further processing

        The list contains the attributes

          basename - the name of the md file without path
          counter - the counter in which the entry appears in the yaml file
          destination - the destination to which the file is copied
          dirname - the path without the basename
          format - the format (md for markdown)
          indent - a default indent that is used for easy printing in hierarchical format
          kind - section or header (a section is a document)
          level - the level this entry occurs
          name - if its a section it defines the section name
          path - the parent path
          prefix - the file prefix (http* or file*)
          title - this is tha basename (we need to add a new mdtitle)
          topic - not used so far
          uri - the location wheer to find the file


    Not implemented are the following features:

    bookmanager YAML pdfget [--force]

        The command searches for all documents within the markdown document and
        fetches them so the document can be created locally. In contrast to the
        get command this command only takes PDF documents as input. The output
        will be a PDF document only.

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
    arguments["FORMAT"] = arguments["--format"] or "epub"
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

    elif arguments.list and (arguments.FORMAT in ["csv"]):

        details = arguments["--details"]
        book.list("csv", details)

    elif arguments.list and (arguments.FORMAT in ["jstree"]):

        book.list("jstree")


    elif arguments.list and (arguments.FORMAT in ["list"]):

        book.list("list")

    elif arguments.check:

        book.check()

    elif arguments["get"]:

        output = arguments["--format"] or "epub"

        if output not in ["epub", "pdf", "md", "markdown"]:
            print(f"Error: format {output} not supported")
            sys.exit(1)

        book.cover()
        book.download(force)
        book.level()
        book.generate(output)

    elif arguments["download"]:

        book.download(force)

    elif arguments.urls:

        book.urls()

    elif arguments.epub:

        book.cover()
        book.generate("epub")

    elif arguments.pdf:

        book.cover()
        book.generate("pdf")

    elif arguments.html:

        book.generate("html")

    elif arguments.docx:

        book.generate("docx")

    elif arguments.md:

        book.generate("md")

    elif arguments.tex:

        book.generate("tex")

    elif arguments.level:

        book.level()


if __name__ == '__main__':
    main()
