#!/usr/bin/env python

"""
Pandoc filter to create lists of all kinds
"""

from pandocfilters import toJSONFilters, walk, Str, Plain, Link, BulletList, Para, RawInline
from functools import reduce
from copy import deepcopy
import io
import sys
import codecs
import json
import re
import unicodedata
import subprocess

collections = {}
headers = [0, 0, 0, 0, 0, 0]
headers2 = [0, 0, 0, 0, 0, 0]

def stringify(x, format):
    """Walks the tree x and returns concatenated string content,
    leaving out all formatting.
    """
    result = []

    def go(key, val, format, meta):
        if key in ['Str', 'MetaString']:
            result.append(val)
        elif key == 'Code':
            result.append(val[1])
        elif key == 'Math':
            # Modified from the stringify function in the pandocfilter package
            if format == 'latex':
                result.append('$' + val[1] + '$')
            else:
                result.append(val[1])
        elif key == 'LineBreak':
            result.append(" ")
        elif key == 'Space':
            result.append(" ")
        elif key == 'Note':
            # Do not stringify value from Note node
            del val[:]

    walk(x, go, format, {})
    return ''.join(result)

def collect(key, value, format, meta):
    global headers

    # Is it a header? Keep the correct numbered headers in the headers array
    if key == 'Header':
        [level, [id, classes, attributes], content] = value
        if 'unnumbered' not in classes:
            headers[level - 1] = headers[level - 1] + 1
            for index in range(level, 6):
                headers[index] = 0

    # Is it a link with a right tag?
    elif key == 'Span':

        # Get the Span
        [[anchor, classes, other], text] = value

        # Is the anchor correct?
        result = re.match('^([a-zA-Z][\w.-]*):([\w.-]+)$', anchor)
        if result:
            global collections

            # Compute the name
            name = result.group(1)

            # Compute the identifier
            identifier = result.group(2)

            # Store the new item
            string = stringify(deepcopy(text), format)
            
            # Prepare the names
            names = []

            # Add the atomic name to the list
            names.append(name)

            # Prepare the latex output
            if format == 'latex':
               latex = '\\phantomsection\\addcontentsline{' + name + '}{figure}{' + string + '}'

            # Loop on all the headers
            for i in [0, 1, 2, 3, 4, 5]:
                if headers[i] > 0:
                    # Add an alternate name to the list
                    altName = name + ':' + '.'.join(map(str, headers[:i+1]))
                    names.append(altName)
                    if format == 'latex':
                       # Complete the latex output
                       latex = latex + '\\phantomsection\\addcontentsline{' + altName + '}{figure}{' + string + '}'
                       latex = latex + '\\phantomsection\\addcontentsline{' + altName + '_}{figure}{' + string + '}'
                else:
                    break

            for name in names:
                # Prepare the new collections if needed
                if name not in collections:
                    collections[name] = []
                collections[name].append({'identifier': identifier, 'text': string})

            # Special case for LaTeX output
            if format == 'latex':
                text.insert(0, RawInline('tex', latex))
                value[1] = text

def listof(key, value, format, meta):
    global headers2

    # Is it a header?
    if key == 'Header':
        [level, [id, classes, attributes], content] = value
        if 'unnumbered' not in classes:
            headers2[level - 1] = headers2[level - 1] + 1
            for index in range(level, 6):
                headers2[index] = 0

    # Is it a paragraph with only one string?
    if key == 'Para' and len(value) == 1 and value[0]['t'] == 'Str':

        # Is it {tag}?
        result = re.match('^{(?P<name>(?P<prefix>[a-zA-Z][\w.-]*)(?P<section>\:((?P<sharp>#(\.#)*)|(\d+(\.\d+)*)))?)}$', value[0]['c'])
        if result:

            prefix = result.group('prefix')

            # Get the collection name
            if result.group('sharp') == None:
                name = result.group('name')
            else:
                level = (len(result.group('sharp')) - 1) // 2 + 1
                name = prefix + ':' + '.'.join(map(str, headers2[:level]))

            # Is it an existing collection
            if name in collections:

                if format == 'latex':
                    # Special case for LaTeX output
                    if 'toccolor' in meta:
                        linkcolor = '\\hypersetup{linkcolor=' + stringify(meta['toccolor']['c'], format) + '}'
                    else:
                        linkcolor = '\\hypersetup{linkcolor=black}'
                    if result.group('sharp') == None:
                        suffix = ''
                    else:
                        suffix = '_'
                    return Para([RawInline('tex', linkcolor + '\\makeatletter\\@starttoc{' + name + suffix + '}\\makeatother')])

                else:
                    # Prepare the list
                    elements = []

                    # Loop on the collection
                    for value in collections[name]:

                        # Add an item to the list
                        if pandocVersion() < '1.16':
                            # pandoc 1.15
                            link = Link([Str(value['text'])], ['#' + prefix + ':' + value['identifier'], ''])
                        else:
                            # pandoc 1.16
                            link = Link(['', [], []], [Str(value['text'])], ['#' + prefix + ':' + value['identifier'], ''])

                        elements.append([Plain([link])])

                    # Return a bullet list
                    return BulletList(elements)

        # Special case where the paragraph start with '{{...'
        elif re.match('^{{[a-zA-Z][\w.-]*}$', value[0]['c']):
            value[0]['c'] = value[0]['c'][1:]

def pandocVersion():
    if not hasattr(pandocVersion, 'value'):
        p = subprocess.Popen(['pandoc', '-v'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out, err = p.communicate()
        pandocVersion.value = re.search(b'pandoc (?P<version>.*)', out).group('version').decode('utf-8')
    return pandocVersion.value


def main():
    toJSONFilters([collect, listof])

if __name__ == '__main__':
    main()

