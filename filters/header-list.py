#!/usr/bin/env python

from pandocfilters import toJSONFilter, Emph, Para, Strong, Str

# pandoc -s -t native test.md
# pandoc test.md --filter ./header-list.py  -s  -t markdown

def behead(key, value, format, meta):
  if key == 'Header' and value[0] == 1:
    # return Para([Strong(value[2])])
    return Para([Strong(value[2])])
  elif key == 'Str':
    return Str(value.upper())


if __name__ == "__main__":
  toJSONFilter(behead)
