"""bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager url download YAML [--format=FORMAT]
  bookmanager url check YAML [--format=FORMAT]
  bookmanager url list YAML [--format=FORMAT]
  bookmanager list YAML [--format=FORMAT]
  bookmanager epub YAML
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

"""
from bookmanager.config import Config
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.common.util import banner, path_expand
from cloudmesh.shell.command import map_parameters
from cloudmesh.common.dotdict import dotdict
from docopt import docopt
from pprint import pprint
from bookmanager.util import download

import requests

debug = False

def main():
    arguments = dotdict(docopt(__doc__))
    arguments["FORMAT"] = arguments["--format"]

    pprint(arguments)

    config = Config(config=arguments.YAML)


    if arguments.info:

        pprint(config.book)
        pprint(config.variables)

    elif arguments.list and (arguments.FORMAT in ["md", "markdown"]):

        banner("MARDOWN")

        result = \
            config.flatten(
                book="My Book",
                title="- {book}",
                section="{indent}- [ ] [{topic}]({url}) {level}",
                header="{indent}- [ ] {topic} {level}",
                indent="  "
            )

        print(config.output(result, kind="text"))

    elif arguments.list and (arguments.FORMAT in ["list"]):

        banner("LITS LIST")

        result = \
            config.flatten(
                book="My Book",
                title="- {book}",
                section="{indent}- [ ] [{topic}]({url}) {level}",
                header="{indent}- [ ] {topic} {level}",
                indent="  "
            )

        print(config.output(result, kind="list"))

    elif arguments.url and arguments.check:

        result = \
            config.flatten(
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

    elif arguments.url and arguments.download:

        result = \
            config.flatten(
                book="",
                title="",
                section="{url}",
                header="",
                indent=""
            )

        for entry in result:
            if entry["kind"] == "section":
                pprint (entry)
                url = entry["url"]
                path = entry["path"]
                path = f"./dist{path}"
                download(url, path)



    elif arguments.url and arguments.list:

        banner("URL")

        if arguments.FORMAT in ["md", "markdown"]:
            kind = "text"
        else:
            kind = "list"


        result = \
            config.flatten(
                book="",
                title="",
                section="{url}",
                header="",
                indent=""
            )

        print (result)

        print('\n'.join(config.output(result, kind="url")))


    elif arguments.epub:

        banner("Creating Epub")

        result = \
            config.flatten(
                book="",
                title="",
                section="{url}",
                header="",
                indent=""
            )

        files = []
        for entry in result:
            if entry["kind"] == "section":
                url = entry["url"]
                path = entry["path"]
                basename=entry["basename"]
                local = path_expand(f"./dist{path}/{basename}")
                entry["local"] = local
                files.append(local)

        banner("Finding Contents")

        print ("Number of included Sections:",  len(result))

        banner("Creating Command")

        files = " ".join(files)
        command = f"pandoc {files}"
        print(command)



if __name__ == '__main__':
    main()
