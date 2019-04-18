from os.path import dirname
from pathlib import Path

import oyaml as yaml
# from bookmanager.yaml_parser_ok import json_flatten
from deprecated.yaml_parser import json_flatten
from cloudmesh.common.FlatDict import flatten as dict_flatten
# from cloudmesh.DEBUG import VERBOSE
from cloudmesh.common.util import path_expand
from munch import munchify


# noinspection PyPep8
class Config(object):
    __shared_state = {}

    def __init__(self, config='./toc.yaml'):
        """
        Initialize the Config class.

        :param config: A local file path to cloudmesh yaml config
            with a root element `cloudmesh`. Default: `.toc.yaml`
        
        Example:
        
        ---
        - BOOK:
          - "{b516}/preface.md"
          - INTRODUCTION:
            - "{manager}/other.md"
          - CLOUD:
            - "{manager}/other.md"
            - AWS:
              - "{manager}/other.md"
              - "i {manager}"
              - "r {manager}"
              - "p {manager}/test.py"
          - DEVOPS:
            - "{manager}/other.md"
            - ANSIBLE:
              - "{manager}/other.md"
              - "i {manager}"
              - "r {manager}"
              - "p {manager}/test.py"
        
        """

        self.__dict__ = self.__shared_state
        if "data" not in self.__dict__:
            # VERBOSE("Load config")

            self.config_path = Path(path_expand(config)).resolve()
            self.config_folder = dirname(self.config_path)

            with open(self.config_path, "r") as content:
                self.data = yaml.load(content, Loader=yaml.SafeLoader)

            self.variables = dict(self.data)
            keys = self.variables.keys()
            del self.variables['BOOK']

            self.book = list(self.data['BOOK'])
            self.flat = munchify(self.variables)
            self.book = self.spec_replace(self.book, self.variables)
            self.variables = dict_flatten(self.variables, sep=".")

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

    def flatten(self,
                book="BOOK",
                title="{book}",
                section="{parent}/{key}",
                header="{parent}/{key}",
                indent=""):
        result = json_flatten(self.book,
                              book=book,
                              title=title,
                              section=section,
                              header=header,
                              level=-1,
                              indent=indent)
        return result

    def dict(self):
        return self.data

    def output(self, result, kind="text"):
        content = []
        for entry in result:
            text = entry["output"].format(**entry)
            content.append(text)

        if kind in ["text"]:
            return '\n'.join(content)

        if kind in ['url']:
            out = []
            for entry in content:
                # print (entry)
                if entry != "":
                    out.append(entry)
            return out

        else:
            return content

    def __str__(self):
        return yaml.dump(self.data, default_flow_style=False, indent=2)

    def get(self, key, default=None):
        """
        A helper function for reading values from the config without
        a chain of `get()` calls.

        Usage:
            mongo_conn = conf.get('db.mongo.MONGO_CONNECTION_STRING')
            default_db = conf.get('default.db')
            az_credentials = conf.get('data.service.azure.credentials')

        :param default:
        :param key: A string representing the value's path in the config.
        """
        return self.data.get(key, default)

    def __getitem__(self, item):
        """
        gets an item form the dict. The key is . separated
        use it as follows get("a.b.c")
        :param item:
        :type item:
        :return:
        """
        if "." in item:
            keys = item.split(".")
        else:
            return self.data[item]
        element = self.data[keys[0]]
        for key in keys[1:]:
            element = element[key]
        return element
