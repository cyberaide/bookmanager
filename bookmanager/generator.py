"""bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager list [YAML]


Arguments:
  YAML   the yaml file

Options:
  -h --help

Description:

    TBD

"""
from bookmanager.config import Config
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.common.dotdict import dotdict
from docopt import docopt
from pprint import pprint

debug = False

def main():
    arguments = dotdict(docopt(__doc__))

    VERBOSE(arguments)

    config = Config(config=arguments.YAML)

    VERBOSE(config.book)
    VERBOSE(config.variables)

    # print(config.flatten(output="{path}/{name}"))

    # print()
    # print(config.flatten(output="{parent}/{key} "))
    # print()
    # print(config.flatten(output="{counter} {parent}/{key} "))
    # print()

    result = \
        config.flatten(
            book="My Book",
            title="- {book}",
            section="{indent}- [ ] [{topic}]({url}) {level}",
            header="{indent}- [ ] {topic} {level}",
            indent="  "
        )

    #print("\n".join(result))

    pprint (result)

    print (len(result))

    print(config.output(result, kind="text"))
    print(config.output(result, kind="list"))

    '''
    print (config)

    print (d)
    '''


if __name__ == '__main__':
    main()
