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

    print(
        config.flatten(
            output="{indent}- [ ] [{topic}]({url}) {level} {headding}",
            header="{indent}- [ ] {topic} {level} {headding}",
            indent=".."
        )
    )
    # print()

    '''
    print (config)

    print (d)
    '''


if __name__ == '__main__':
    main()
