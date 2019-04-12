import oyaml as yaml
from pprint import pprint


def process_image(link):
    pass


def process_program(link):
    pass


def process_dir(link):
    pass


counter = -1


def flatten_json(data, output="{counter} {parent}/{key}"):
    global counter
    counter = -1
    r = len(yaml.dump(data).split("\n"))

    out = ['undefined'] * r

    def flatten(x, parent='', name='', output=output):
        global counter
        if type(x) is dict:
            for a in x:
                counter = counter + 1
                key = list(x.keys())[0]
                # key = a.keys()[0]

                display = output.format(**locals(), counter=counter)
                out[counter] = display
                flatten(x[a], parent=f"{parent}/{a}", name=f"{name}{a}/",
                        output=output)
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, parent=f"{parent}", name=f"{name}{i}/",
                        output=output)
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

            display = output.format(**locals(), counter=counter)
            out[counter] = display

    flatten(data)

    return out[:counter + 1]
