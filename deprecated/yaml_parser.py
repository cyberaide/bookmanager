import os

import oyaml as yaml


def process_image(link):
    pass


def process_program(link):
    pass


def process_dir(link):
    pass


counter = 1


def clean_path(repos):
    for repo in repos:
        if repo["path"].startswith("/"):
            repo["path"] = repo["path"][1:]
    return repos


def json_flatten(data,
                 book="BOOK",
                 title="{title}",
                 section="{counter} {path} {topic} {url} {line}",
                 header="{counter} {path} {topic} {url} {line}",
                 level=0,
                 indent=""):
    verbose = False
    global counter
    counter = 0
    r = len(yaml.dump(data).split("\n"))

    out = ['undefined'] * r
    out[0] = {
        "url": "",
        "topic": book,
        "title": title,
        "book": book,
        "output": title,
        "header": header,
        "level": level,
        "indent": indent,
        "kind": "title",
        "path": "."
    }

    def _flatten(entry,
                 book=book,
                 title=title,
                 path='',
                 name='',
                 section=section,
                 header=header,
                 level=level,
                 indent=indent):
        global counter
        if type(entry) is dict:
            for a in entry:
                level = level + 1
                counter = counter + 1
                key = list(entry.keys())[0]
                topic = a

                d = {
                    "title": title,
                    "name": a,
                    "kind": "header",
                    "output": header,
                    "url": "",
                    "line": key,
                    "basename": f"{topic}",
                    "path": f"{path}/{topic}",
                    "counter": counter,
                    "level": level,
                    "indent": level * indent,
                    "topic": a.replace("-", " ")
                }
                if verbose:
                    print("-----", d)

                # display = header.format(**d)
                # out[counter] = display
                out[counter] = d

                _flatten(entry[a],
                         book=book,
                         title=title,
                         path=f"{path}/{a}",
                         name=f"{name}{a}/",
                         section=section,
                         header=header,
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
                         section=section,
                         header=header,
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
                "output": section,
                "kind": "section",
                "url": location,
                "line": entry,
                "basename": basename,
                "path": path,
                "counter": counter,
                "name": name,
                "level": level,
                "indent": level * indent,
                "topic": name.replace("-", " ").capitalize()
            }
            if verbose:
                print("     >>>>>", d)

            # result = output.format(**d)
            # out[counter] = result
            out[counter] = d

    try:
        _flatten(
            data,
            book=book,
            title=title,
            section=section,
            header=header,
            level=level,
            indent=indent)
    # except KeyError as e:
    except Exception as e:
        print()
        print(f"ERROR: The key {e} could not be found")

    d = out[:counter + 1]

    return clean_path(d)
