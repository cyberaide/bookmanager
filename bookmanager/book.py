import os
import sys
from pathlib import Path
from pprint import pprint
from shutil import copyfile


import pkg_resources
import requests
from bookmanager.cover import Cover
from bookmanager.util import cat_bibfiles, find_unique_name
from bookmanager.util import create_metadata, create_css
from bookmanager.util import create_section
from bookmanager.util import download as page_download
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.util import banner, path_expand, readfile
from tabulate import tabulate
from bookmanager.document import Documents

debug = False

# noinspection PyPep8
class Book:

    def __init__(self, arguments):

        self.docs = Documents()

        self.docs.load(arguments.YAML, "BOOK")


        self.metadata = self.docs.metadata
        self.arguments = arguments

    def printer(self,
                section="{counter:3} {level:3} {path:20} {indent} - [ ] {title}",
                header="{counter:3} {level:3} {path:20} {indent} - [ ] {title}"
                ):

        r = self.docs.printer(
                    section="{counter:3} {level:3} {path:20} {indent} - [ ] {title}",
                    header="{counter:3} {level:3} {path:20} {indent} - [ ] {title}"
                    )

        print('\n'.join(r))


    def list(self, output, details):
        banner("list")

        banner("MARDOWN")

        if output == "markdown":

            if details:
                self.printer(
                    section="{level:3} {path:20} {kind} {indent}- [ ] [{topic}]({url})",
                    header="{level:3} {path:20} {kind} {indent}- [ ]  {topic}",
                )
            else:
                self.printer(
                    section="{indent}- [ ] [{topic}]({url})",
                    header="{indent}- [ ]  {topic}",
                )



    def check(self):

        banner("check")

        for entry in self.docs.entries:
            if entry.kind == "section":
                if entry.uri.startswith("http"):
                    print(entry.uri, end="")
                    response = requests.get(entry.uri)
                    if response.status_code < 400:
                        print(" -> ok")
                    else:
                        print("error", response.status_code)

    def download(self, force):

        banner("get")

        for entry in self.docs.entries:
            if entry["kind"] == "section":
                print(entry.level * "   ", entry.counter, entry.title, end=' ')
                print('...', end=' ')

                entry.destination = find_unique_name(entry, self.docs.entries)

                page_download(entry.uri, entry.destination, entry.level, force)
                print()
            elif entry.kind == 'header':
                print(entry.level * "   ", entry.counter, entry.title)

    def urls(self):

        banner("URL")

        if self.arguments.FORMAT in ["md", "markdown"]:
            kind = "text"
        else:
            kind = "list"

        urls = []
        for entry in self.docs.entries:
            if entry.kind == "section":

                urls.append(entry.uri)

        print('\n'.join(urls))


    def generate(self, output):

        banner(f"Creating {output}")

        files = []
        for entry in self.docs.entries:

            if entry.kind in ["section", "header"]:
                url = entry.url
                path = entry.path
                basename = entry.basename
                local = entry.destination
                files.append(local)

        banner("Finding Contents")

        print("Number of included Sections:", len(self.docs.entries))

        banner("Creating Command")

        files = " ".join(files)

        # metadata["stylesheet"] = path_expand(metadata["stylesheet"])
        title = self.metadata["title"]

        if output == "epub":

            dirs = []
            for section in self.docs.entries:
                if section["kind"] == "section":
                    # pprint(section)
                    path = section["path"]
                    dirs.append(path_expand(f"./dest/book/{path}"))
            dirs = set(dirs)
            # dirs = find_image_dirs(directory='./dest')

            create_metadata(self.metadata, "./dest/book/metadata.txt")
            create_css(self.metadata, "./dest/book/epub.css")

            # pprint(self.metadata)

            directories = (":".join(dirs))
            metadata = path_expand("./dest/book/metadata.txt")
            filename = self.metadata["filename"]

            #
            # ad bibfile if bib was found
            #
            cat_bibfiles("./dest", "./dest/all.bib")

            bib = path_expand("./dest/all.bib")
            csl = path_expand("./dest/book/ieee-with-url.csl")
            bibfile = f"--filter pandoc-citeproc --metadata link-citations=true --bibliography={bib} --csl={csl}"
            all_bibs = readfile("./dest/all.bib")
            css_style = pkg_resources.resource_filename("bookmanager",'template/epub/ieee-with-url.csl')

            # print (css_style)
            # print(csl)

            copyfile(css_style, path_expand("./dest/book/ieee-with-url.csl"))

            if "@" not in all_bibs:
                bibfile = ""

            # "MARKDOWN-OPTIONS=--verbose  $(MERMAID) --filter pandoc-crossref -f markdown+header_attributes -f markdown+smart -f markdown+emoji --indented-code-classes=bash,python,yaml"

            markdown = "--verbose --filter pandoc-crossref -f markdown+emoji --indented-code-classes=bash,python,yaml"
            options = "--toc --toc-depth=6  --number-sections"
            resources = f"--resource-path={directories}"
            epub = path_expand(f"./dest/{filename}")
            # noinspection PyPep8
            command = f'cd dest/book; pandoc {options} {markdown} {resources} {bibfile} -o {epub} {files} {metadata}'
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

        def convert_level(entry):

            pandoc_level = entry.level + 1
            tmp = str(Path(self.docs.metadata["dest"]) / "tmp.md")
            command = "pandoc --base-header-level={pandoc_level} -o {tmp} {destination} > log.txt".format(
                **entry, tmp=tmp, pandoc_level=pandoc_level)
            sys.stdout.flush()

            os.system(command)
            command = "cp {tmp} {destination} > log.txt".format(**entry, tmp=tmp)
            os.system(command)
            os.system(f"rm -f {tmp}")
            os.system("rm -f log.txt")


        banner("Creating Level")

        title = self.docs.metadata["title"]


        def PRINT(entry, end="\n"):
            print(entry.level * "   ", entry.counter, entry.title, entry.uri, end=end)


        # pprint(self.docs.entries)


        for entry in self.docs.entries:

            if entry.kind == "header":
                PRINT(entry)
                create_section(entry.destination, entry.title, entry.level + 1)

            elif entry.kind == "section":

                PRINT(entry, end=' ')
                sys.stdout.flush()

                # n = find_smalest_headers(readfile(entry["local"]))
                # print (n, end="")
                # out = reduce_headers(readfile(entry["local"]), n, entry.level)
                # writefile(entry["local"], "\n".join(out))

                print(entry.level, end="")
                convert_level(entry)

                print('...', end=' ')
                sys.stdout.flush()
                print()

    def cover(self):

        cover = Cover()

        metadata = dotdict(self.docs.metadata)

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
