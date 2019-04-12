import oyaml as yaml
from pprint import pprint
import os


def process_image(link):
    pass


def process_program(link):
    pass


def process_dir(link):
    pass


counter = -1


def json_flatten(data,
                 output="{counter} {path} {url} {line}",
                 header = "{counter} {path} {url} {line}",
                 indent_level=0,
                 indent=""):

    global counter
    counter = -1
    r = len(yaml.dump(data).split("\n"))

    out = ['undefined'] * r

    def _flatten(entry, path='', name='', output=output, header=header, level=0, indent_level = indent_level, indent=indent):
        global counter
        if type(entry) is dict:
            for a in entry:
                counter = counter + 1
                key = list(entry.keys())[0]
                # key = a.keys()[0]
                topic=f"{path} {key}"[1:]

                d = {
                    "name": a,
                    "headding": True,
                    "url": "",
                    "line": key,
                    "basename": "",
                    "path": path,
                    "counter": counter,
                    "level": level,
                    "indent": level * indent,
                    "topic": a.replace("-", " ")

                }
                print("-----", d)

                display = header.format(**d)
                out[counter] = display
                _flatten(entry[a],
                         path=f"{path}/{a}",
                         name=f"{name}{a}/",
                         output=output,
                         header=header,
                         indent_level=indent_level,
                         level=level+1)
        elif type(entry) is list:
            i = 0
            for a in entry:
                _flatten(a,
                         path=f"{path}",
                         name=f"{name}{i}/",
                         output=output,
                         header=header,
                         indent_level=indent_level,
                         level=level+1,
                         indent=indent)
                i += 1
        else:
            counter = counter + 1
            # out[counter] = (line, f"{path}/{line}", name, counter)
            if entry.startswith("i "):
                entry = entry.replace("i ", "")
                process_image(entry)
            elif entry.startswith("p "):
                entry = entry.replace("p ", "")
                process_program(entry)
            elif entry.startswith("r "):
                entry = entry.replace("r ", "")
                process_dir(entry)

            location = entry
            key = entry
            basename = os.path.basename(entry)
            name = basename.replace(".md", "")

            d = {
                "headding": False,
                "url": location,
                "line": entry,
                "basename": basename,
                "path": path,
                "counter": counter,
                "name": name,
                "level": level,
                "indent": level  * indent,
                "topic": name.replace("-"," ").capitalize()
            }
            print("     >>>>>", d)

            result = output.format(**d)
            out[counter] = result

    try:
        _flatten(data, output=output, header=header)
    # except KeyError as e:
    except Exception as e:
        print()
        print(f"ERROR: The key {e} could not be found")

    return out[:counter + 1]
