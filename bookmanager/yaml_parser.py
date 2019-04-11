import oyaml as yaml

def process_image(link):
    pass


def process_program(link):
    pass


def process_dir(link):
    pass


counter = -1
def flatten_json(data, output="{counter} {parent}/{key}"):

    global counter
    r = len(yaml.dump(data).split("\n"))

    out = ['undefined'] * r

    def flatten(x, parent='', name='', output=output):
        global counter
        if type(x) is dict:
            for a in x:
                counter = counter + 1
                key = list(x.keys())[0]
                #key = a.keys()[0]

                display = output.format(**locals(), counter=counter)
                out[counter] = (counter, display)
                flatten(x[a], parent=f"{parent}/{a}", name=f"{name}{a}/", output=output)
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, parent=f"{parent}", name=f"{name}{i}/", output=output)
                i += 1
        else:
            counter = counter + 1
            # out[counter] = (x, f"{parent}/{x}", name, counter)
            if x.startswith("i "):
                x = x.replace("i ", "")
                process_image(x)
            elif x.startswith("p "):
                x = x.replace("p ", "")
                process_program(x)
            elif x.startswith("r "):
                x = x.replace("r ", "")
                process_dir(x)
            key = x

            display =  output.format(**locals(), counter=counter)
            out[counter] = (counter, display)

    flatten(data)

    return out[:counter+1]

def new_find_sources(d,
                 parent='',
                 sep='/',
                 sources=None,
                 headings=None,
                 output="{indent} {parent}"):
    sources = []
    headings = []
    all = []

    def _flatten(d, parent='', indent=0, sep='/', output=output):
        if type(d) == list:
            for entry in d:
                _flatten(entry, indent=indent + 1, parent=parent)
        elif type(d) == dict:
            key = list(d.keys())[0]
            child = d[key]
            parent = f"{parent}{sep}{key}"
            _flatten(child, parent=parent, indent=indent)
            headings.append(output.format(indent=indent,
                                          parent=parent))
            all.append(output.format(indent=indent,
                                          parent=parent))

        else:
            if d.startswith("i "):
                d = d.replace("i ", "")
                process_image(d)
            elif d.startswith("p "):
                d = d.replace("p ", "")
                process_program(d)
            elif d.startswith("r "):
                d = d.replace("r ", "")
                process_dir(d)
            #sources.append(f"{indent} {parent}/{d}")


            line = output.format(indent=indent,
                                 parent=parent) + f"/{d}"
            sources.append(line)
            all.append(line)

    _flatten(d, parent='', sep='/')

    return sources, reversed(headings), reversed(all)


def find_sources(d,
                 parent='',
                 sep='/',
                 sources=None,
                 headings=None,
                 output="{indent} {parent}"):
    sources = []
    headings = []
    all = []

    def _flatten(d, parent='', indent=0, sep='/', output=output):
        if type(d) == list:
            for entry in d:
                _flatten(entry, indent=indent + 1, parent=parent)
        elif type(d) == dict:
            key = list(d.keys())[0]
            child = d[key]
            parent = f"{parent}{sep}{key}"
            _flatten(child, parent=parent, indent=indent)
            headings.append(output.format(indent=indent,
                                          parent=parent))
            all.append(output.format(indent=indent,
                                          parent=parent))

        else:
            if d.startswith("i "):
                d = d.replace("i ", "")
                process_image(d)
            elif d.startswith("p "):
                d = d.replace("p ", "")
                process_program(d)
            elif d.startswith("r "):
                d = d.replace("r ", "")
                process_dir(d)
            #sources.append(f"{indent} {parent}/{d}")


            line = output.format(indent=indent,
                                 parent=parent) + f"/{d}"
            sources.append(line)
            all.append(line)

    _flatten(d, parent='', sep='/')

    return sources, reversed(headings), reversed(all)
