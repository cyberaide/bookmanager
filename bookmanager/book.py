import os
import sys
import time
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
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.FlatDict import FlatDict2

from cloudmesh.common.util import banner, path_expand, readfile, writefile
from tabulate import tabulate
from bookmanager.document import Documents
import shlex

debug = False

# noinspection PyPep8
class Book:

    def print_command(self, command):
        if self.verbose:
            banner("COMMAND")
            _command = "\n".join(shlex.split(command))
            print(_command)


    def __init__(self, arguments):

        self.docs = Documents()
        self.verbose = False

        self.docs.load(arguments.YAML, "BOOK")


        self.metadata = self.docs.metadata
        if "filename" not in self.metadata:
            self.metadata["filename"] = arguments.YAML
        self.arguments = arguments

    def printer(self,
                section="{counter:3} {level:3} {path:20} {indent} - [ ] {documenttitle} {title}",
                header="{counter:3} {level:3} {path:20} {indent} - [ ] {documenttitle} {title}"
                ):

        r = self.docs.printer(
                    section=section,
                    header=header
                    )

        print('\n'.join(r))


    def list(self, output="markdown", details=False, csvchar=","):
        banner("list")

        #
        # UPDATE THE DOCUMENT TITLE
        #
        self.get_titles()

        #
        # PRINT THE LIST
        #

        if output == "markdown":

            banner("MARDOWN")

            if details:

                self.printer(
                    section="{level:3} {path:20} {kind} {indent}- [ ] {documenttitle} [{topic}]({uri})",
                    header="{level:3} {path:20} {kind} {indent}- [ ] {documenttitle} {topic}",
                )
            else:

                self.printer(
                    section="{indent}- [ ] {documenttitle}",
                    header="{indent}- [ ]  {documenttitle}",
                )

        elif output=="list":

            pprint(self.docs.entries)

        elif output=="csv":

            r = self.docs.printer(
                section="{counter},{level},{path},{kind},{indent},{documenttitle},{title},{topic},{uri}",
                header="{counter},{level},{path},{kind},{indent},{documenttitle},{title},{topic},{uri}",
            )

            print('\n'.join(r))

        elif output=="jstree":

            """
            <code>[
              { "id": "root", "parent": "#", "text": "ROOT" },
              { "id": "external", "parent": "root", "text": "external" },
              { "id": "teachers", "parent": "root", "text": "teachers" },
              { "id": "companyBV", "parent": "root", "text": "company BV" },
              { "id": "buying", "parent": "companyBV", "text": "Buying" },
              { "id": "finance", "parent": "companyBV", "text": "finance" },
              { "id": "buyingCenter", "parent": "buying", "text": "buying center" },
              { "id": "buyingGeneric", "parent": "buying", "text": "buying generic" },
              { "id": "buyingSCenter", "parent": "buying", "text": "buying service center" }
            ]</code>
            On client side just feed it to the jsTree config:

            <code>$('#jstree').jstree({
                core: {
                  data: data
                }
            })</code>
            """

            banner("JSTREE")

            tree = []

            for entry in self.docs.entries:
                if entry.kind == "header":
                    if "/" in entry.path:
                        parent = "/".join(entry.path.split("/")[:-1])
                    else:
                        parent = "#"
                    e = {
                        "id": entry.path,
                        "parent": parent,
                        "text": entry.title
                    }
                    tree.append(e)

                elif entry.kind == "section":
                    if "/" in entry.path:
                        parent = "/".join(entry.path.split("/")[:-1])
                    else:
                        parent = "#"
                    e = {
                        "id": entry.path + "_" + entry.title.replace("-", "_"),
                        "parent": entry.path,   # THIS IS A BUG AND DOES NOT WORK IF PARENT IS A SECTION
                        "text": entry.documenttitle
                    }

                    tree.append(e)
            for entry in tree:
                print (entry)

            return tree


    def check(self):

        banner("check")

        for entry in self.docs.entries:
            if entry.kind == "section":
                if entry.uri.startswith("http"):
                    print(entry.uri, end="")
                    response = requests.get(entry.uri, headers={'Cache-Control': 'no-cache'})
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

                page_download(entry.uri, entry.destination, entry.level, force, self.docs.variables)


                print()
            elif entry.kind == 'header':
                print(entry.level * "   ", entry.counter, entry.title)

        self.get_titles()

    def find_title(self, markdown):
        """
        must be called after download
        :param markdown:
        :return:
        """
        title = None
        with open(markdown, "r") as f:
            lines = f.readlines()
            previous=lines[0] or ""
            found = None

            for line in lines:
                if "# " in line:
                    found = line.split("# ", 1)[1]

                elif line[0] in ["=-~^"]:
                    found = previous
                if found:
                    if "[" in found:
                        title = found.split("[")[0].strip()
                    return title
                previous = line
        return title

    def get_titles(self):

        #
        # this function must be called after download
        #
        banner("get titles")

        for entry in self.docs.entries:
            if entry["kind"] == "section":
                #
                # find the title in teh downloaded document
                #
                title = self.find_title(entry.destination)
                if title == None:
                    entry.documenttitle = entry.title
                else:
                    entry.documenttitle = title

            elif entry.kind == 'header':
                entry.documenttitle = entry.title
        if self.verbose:
            pprint (self.docs.entries)

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

        banner(f"Creating {output}", c="&")

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

        dirs = []
        for section in self.docs.entries:
            if section["kind"] == "section":
                # pprint(section)
                path = section["path"]
                dirs.append(path_expand(f"./dest/book/{path}"))
        dirs = set(dirs)
        # dirs = find_image_dirs(directory='./dest')

        if output in ["pdf"]:
            create_metadata(self.metadata, "./dest/book/metadata.txt", kind="latex")
        else:
            create_metadata(self.metadata, "./dest/book/metadata.txt", kind="epub")

        from cloudmesh.common.Shell import Shell
        r = Shell.cat("./dest/book/metadata.txt")
        if self.verbose:
            banner(r)

        create_css(self.metadata, "./dest/book/epub.css")

        directories = (":".join(dirs))
        metadata = path_expand("./dest/book/metadata.txt")
        filename = self.metadata["filename"]

        for file in ["report.bib", "references.bib"]:
            try:
                copyfile(file, f"dest/{file}")
            except:
                pass
        cat_bibfiles("./dest", "./dest/all.bib")

        bib = path_expand("./dest/all.bib")
        csl = path_expand("./dest/book/ieee-with-url.csl")

        bibfile = f" --metadata link-citations=true --bibliography={bib} --csl={csl}"
        all_bibs = readfile("./dest/all.bib")
        css_style = pkg_resources.resource_filename("bookmanager",
                                                    'template/epub/ieee-with-url.csl')

        copyfile(css_style, path_expand("./dest/book/ieee-with-url.csl"))

        if "@" not in all_bibs:
            bibfile = ""

        for f in ['template/latex/listings-setup.tex',
                  'template/latex/eisvogel.latex',
                  'template/empty.md'
                  ]:
            source = pkg_resources.resource_filename("bookmanager", f)
            _filename = os.path.basename(source)
            copyfile(source, f"dest/{_filename}")

        options = "--toc --toc-depth=6  --number-sections --citeproc -F pandoc-crossref --from markdown-smart"
        resources = f"--resource-path={directories}"
        markdown = "--verbose --citeproc --filter pandoc-crossref -f markdown+emoji+smart --indented-code-classes=bash,python,yaml"
        pdf_options = "--verbose -f markdown+emoji+smart --indented-code-classes=bash,python,yaml" \
                      " --include-in-header ./dest/listings-setup.tex --template ./dest/eisvogel --listings"

        # GGGG markdown = "--verbose -f markdown+emoji --indented-code-classes=bash,python,yaml"
        # fonts = '-V mainfonts="DejaVu Sans"'
        pdffonts = ''

        embed = [
            "DejaVuSerif-Bold.ttf",
            "DejaVuSerif-BoldItalic.ttf",
            "DejaVuSerif-Italic.ttf",
            "DejaVuSerif.ttf",
            "DejaVuSerifCondensed-Bold.ttf",
            "DejaVuSerifCondensed-BoldItalic.ttf",
            "DejaVuSerifCondensed-Italic.ttf",
            "DejaVuSerifCondensed.ttf"
        ]
        embed = [
            "OpenSans-Bold.ttf",
            "OpenSans-BoldItalic.ttf",
            "OpenSans-Emoji.ttf",
            "OpenSans-ExtraBold.ttf",
            "OpenSans-ExtraBoldItalic.ttf",
            "OpenSans-Italic.ttf",
            "OpenSans-Light.ttf",
            "OpenSans-LightItalic.ttf",
            "OpenSans-Regular.ttf",
            "OpenSans-Semibold.ttf",
            "OpenSans-SemiboldItalic.ttf",
            "OpenSansEmoji.ttf",
        ]

        # ignoring font embedding
        epubfonts = ''
        #for font in embed:
        #    epubfonts = epubfonts + f' --epub-embed-font=fonts/{font}'

        if output in ["epub"]:

            epub = path_expand(f"./dest/{filename}")
            # noinspection PyPep8
            command = f'cd dest/book; pandoc {options} {markdown} ' \
                      f' {epubfonts} {resources} {bibfile} ' \
                      f' -o {epub} {files}' \
                      f' {metadata}'
            if self.verbose:
                self.print_command(command)

        elif output == "pdf":

            create_metadata(self.metadata, "./dest/book/metadata.txt", kind="latex")

            pdf = path_expand(f"./dest/{filename}").replace(".epub", ".pdf")
            tex = path_expand(f"./dest/{filename}").replace(".epub", ".tex")
            md = path_expand(f"./dest/{filename}").replace(".epub", ".md")
            metadata = "./dest/book/metadata.txt"

            # path= Path("../../bookmanager/bookmanager/template/latex/eisvogel").resolve()
            book= "-V titlepage=true"
            #latex = f"--template {path} --pdf-engine=xelatex"
            # latex = f"--pdf-engine=pdflatex --indented-code-classes=bash,python,yaml"
            latex = f"--pdf-engine=pdflatex --indented-code-classes=bash,python,yaml"

            command = f'pandoc' \
                      f' {files} ' \
                      f' --to=markdown > {md}'
            self.print_command(command)
            os.system(command)

            content = readfile(md)
            content = content \
                .replace("µ","micro") \
                .replace(":cloud:","\\faGithub")\
                .replace(":o2:","\\faBug")\
                .replace("\\lstinline!\\faBug!","\\faBug")
            writefile(md, content)

            command = f'pandoc -s {options} {pdf_options} {pdffonts}' \
                      f' {bibfile} {latex} {book} {resources} ' \
                      f' {md} ' \
                      f' {metadata} --from=markdown -o {pdf}'

        elif output == "html":
            metadata = "./dest/metadata.txt"
            options = "--toc --number-sections"
            command = f'pandoc {options} -o ./dest/book.html {files}'

        elif output == "docx":
            metadata = "./dest/metadata.txt"
            options = "--toc --number-sections"
            command = f'pandoc {options} -o ./dest/book.docx {files}'

        elif output in ["md", "markdown"]:
            metadata = "./dest/metadata.txt"
            options = "--toc --number-sections -f markdown+smart"
            command = f'pandoc {options} -o ./dest/book.md {files}'

        elif output in ["tex"]:
            metadata = "./dest/metadata.txt"
            options = "--toc --number-sections"
            command = f'pandoc {options} -o ./dest/book.tex {files}'
        else:
            raise ValueError(f"this output format is not yet supported: {output}")

        if self.verbose:
            banner("COMMAND")
            self.print_command(command)
        os.system(command)
        try:
            os.system("sync")
        except:
            pass

    def level(self):

        def convert_level(entry):

            #destination = entry["destination"]
            #extension = os.path.basename(destination).rsplit(".", 1)[1]
            #if extension in ["yaml", "yml"]:
            #    VERBOSE(destination)
            #    filewrap(f"./dest/book/{destination}", "```", "```")

            pandoc_level = entry.level + 1
            tmp = str(Path(self.docs.metadata["dest"]) / "tmp.md")
            command = "pandoc --shift-heading-level-by={pandoc_level} -o {tmp} {destination} > log.txt".format(
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
