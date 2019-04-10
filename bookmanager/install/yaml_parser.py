

def process_image(link):
    pass


def process_program(link):
    pass


def process_dir(link):
    pass


def find_sources(d,
                 parent='',
                 sep='/',
                 sources=None,
                 headings=None):
    sources = []
    headings = []

    def _flatten(d, parent='', sep='/'):
        if type(d) == list:
            for entry in d:
                _flatten(entry, parent=parent)
        elif type(d) == dict:
            key = list(d.keys())[0]
            child = d[key]
            parent = f"{parent}{sep}{key}"
            _flatten(child, parent=parent)
            headings.append(parent)
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
            sources.append(f"{parent}/{d}")

    _flatten(d, parent='', sep='/')
    return sources, headings
