from pprint import pprint
from pathlib import Path
import oyaml as yaml
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.common.util import readfile
from cloudmesh.common.dotdict import dotdict
from munch import munchify
from cloudmesh.common.FlatDict import flatten as dict_flatten
import os
from collections import Counter


class Document(dotdict):

    def __init__(self):
        self["title"] = None  # The title
        self["name"] = None  # A short name unique for the destination dir
        self["kind"] = "section"  # header section
        self["uri"] = None  # https://
        self["prefix"] = "http"  # https http local
        self["basename"] = None
        self["dirname"] = None
        self["destination"] = None  # where to copy it to
        self["counter"] = 0
        self["level"] = 0
        self["topic"] = None
        self["format"] = None
        self["indent"] = ""


class Documents(object):

    def __init__(self):
        self.entries = []
        self.depth = 0
        self.metadata = []

    def spec_replace(self,
                     book,
                     variables):

        variable_list = dict_flatten(variables, sep=".")

        spec = yaml.dump(book)

        for variable in variable_list:
            value = variable_list[variable]
            token = "{" + variable + "}"
            spec = spec.replace(token, value)

        output = yaml.load(spec, Loader=yaml.SafeLoader)
        return output

    def load(self, filename, base):
        filename = str(Path(filename).resolve())

        text_content = readfile(filename).strip()
        yaml_content = yaml.load(text_content, Loader=yaml.SafeLoader)

        self.metadata = yaml_content['metadata']
        #
        # REPLACE VARIABLES
        #
        book = yaml_content["BOOK"]
        variables = yaml_content
        del variables["BOOK"]

        self.flat = munchify(variables)
        b = self.spec_replace(book, variables)
        transformed = yaml.dump(b)
        # print (transformed)

        lines = transformed.split("\n")

        counter = 0
        for line in lines:
            if len(line) == 0 or line.strip().startswith("#"):
                continue
            doc = Document()
            indent, value = line.split("-", 1)
            indent = int(len(indent) / 2)
            self.depth = max(self.depth, indent)
            doc.level = indent
            doc.counter = counter
            if line.strip().endswith(":"):
                doc.kind = "header"
                doc.title = value.strip()[:-1]

            if doc.kind != "header":
                doc.uri = value.strip()
            self.entries.append(doc)
            counter += 1
        self.local_path_resolve()
        # self.make_local_files_unique()

    def __str__(self):
        data = str(self.__dict__)
        return (data)

    def local_path_resolve(self):
        path_list = [""] * (self.depth + 1)
        for entry in self.entries:
            if entry.kind == "section":

                if entry.uri.startswith("file://"):
                    entry.uri = entry.uri.replace("file://", "")
                    entry.uri = str(Path(entry.uri).resolve())
                entry.dirname = os.path.dirname(entry.uri)
                entry.basename = os.path.basename(entry.uri)
                entry.title, entry.format = entry.basename.split(".")
                entry.format = entry.format.lower()
                entry.path = '/'.join(path_list[:entry.level])

                entry.destination = self.metadata["dest"]
                entry.destination = str(Path(entry.destination).resolve())
                entry.destination = "{destination}/{path}/{basename}".format(
                    **entry)

            elif entry.kind == "header":
                path_list[entry.level] = entry.title
                entry.path = path_list[:entry.level + 1]

                entry.path = '/'.join(entry.path)

                entry.basename = "HEADER-{title}.md".format(**entry)
                entry.format = "md"

                entry.name = "HEADER-{title}".format(**entry)
                entry.prefix = None

                entry.destination = self.metadata["dest"]
                entry.destination = str(Path(entry.destination).resolve())
                # print (path_list)
                entry.destination = "{destination}/{path}/{basename}".format(
                    **entry)
                entry.dirname = os.path.dirname(entry.destination)

                # print(entry)

            entry.indent = "  " * entry.level

    def make_local_files_unique(self):
        ids = []
        locations = []
        for entry in self.entries:
            if entry.kind == "section":
                # print (entry)
                locations.append(entry.destination)
                ids.append(entry.counter)

        # print (ids)
        # pprint (locations)

        counts = Counter(locations)
        # pprint (counts)

        duplicates = {k: v for k, v in counts.items() if v > 1}

        # pprint (duplicates)
        for entry in self.entries:
            if entry.destination in duplicates:
                base, ending = entry.destination.rsplit(".", 1)
                counter = entry.counter
                entry.destination = str(Path(f"{base}-{counter}.{ending}"))



    def printer(self,
                section="{indent} - [ ] {title}",
                header="{indent} - [ ] {title}"
                ):
        content = []
        for entry in self.entries:
            if entry.kind == "header":
                kind = header
            elif entry.kind == "section":
                kind = section
            content.append(kind.format(**entry))
        return content
