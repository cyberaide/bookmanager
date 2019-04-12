import oyaml as yaml
from pprint import pprint
import os

def process_image(link):
    pass


def process_program(link):
    pass


def process_dir(link):
    pass


counter = 1


def json_flatten(data,
                 book="BOOK",
                 title="{title}",
                 output="{counter} {path} {url} {line}",
                 header = "{counter} {path} {url} {line}",
                 indent_level=0,
                 indent=""):

    verbose = True
    global counter
    counter = 0
    r = len(yaml.dump(data).split("\n"))

    out = ['undefined'] * r
    out[0] = title.format(**locals())

    def _flatten(entry,
                 book=book,
                 title=title, path='', name='', output=output, header=header, level=0, indent_level = indent_level, indent=indent):
        global counter
        if type(entry) is dict:
            for a in entry:
                level = level + 1
                counter = counter + 1
                key = list(entry.keys())[0]
                # key = a.keys()[0]
                topic=f"{path} {key}"[1:]

                d = {
                    "title": title,
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
                if verbose:
                    print("-----", d)

                display = header.format(**d)
                out[counter] = display
                _flatten(entry[a],
                         book=book,
                         title=title,
                         path=f"{path}/{a}",
                         name=f"{name}{a}/",
                         output=output,
                         header=header,
                         indent_level=indent_level,
                         level=level,
                         indent=indent)
        elif type(entry) is list:
            i = 0
            level = level + 1
            for a in entry:
                _flatten(a,
                         book=book,
                         title=title,
                         path=f"{path}",
                         name=f"{name}{i}/",
                         output=output,
                         header=header,
                         indent_level=indent_level,
                         level=level,
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
                "title": title,
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
            if verbose:
                print("     >>>>>", d)

            result = output.format(**d)
            out[counter] = result

    try:
        _flatten(
            data,
            book=book,
            title=title,
            output=output,
            header=header,
            indent_level=indent_level,
            indent=indent)
    # except KeyError as e:
    except Exception as e:
        print()
        print(f"ERROR: The key {e} could not be found")

    return out[:counter + 1]
