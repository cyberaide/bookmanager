
# Bookmanager

Bookmanager is a tool to create a publication from a number of sources on the
internet. It is especially useful to create customized books, lecture notes, or
handouts. Content is best integrated in markdown format as it is very fast to
produce the output. At present we only produce epubs, but it will be easy to
also create pdf, html, work, odt and others. As we use pandoc we can support the
formats supported by it.

Planed enhancements:

* customized title page
* integration of Refernces
* proper indentation management based on the indentation in teh yaml file
* automated image management
* font management for epubs

If you like to help get in contagt with Gregor von Laszewski
<laszewski@gmail.com>

```bash
$ pip install cyberaide-bookmanager
```

## Usage
bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager YAML get [--format=FORMAT]
  bookmanager YAML download
  bookmanager YAML level
  bookmanager YAML epub
  bookmanager YAML pdf
  bookmanager YAML html
  bookmanager YAML docx
  bookmanager YAML check [--format=FORMAT]
  bookmanager YAML urls [--format=FORMAT]
  bookmanager YAML list [--format=FORMAT]
  bookmanager info


Arguments:
  YAML   the yaml file

Options:
  -h --help
  -f, --format=FORMAT     [default: markdown]

Description:

    In principal you only need one command at this time. All other commands are
    available for test purposes.

    You can create an epub with

      bookmanager YAML get [--format=FORMAT]

    The command seatches for all images within the markdown documet and fetches
    them so the document can be created locally with the images. We assume all
    images in the md document are for now not specified via http locations but
    via relative locations.

    To view the document use your favourite ePub Reader

    Other commands include:

      bookmanager YAML download [--format=FORMAT]

        downloads the urls into the ./dist directory for local processing

      bookmanager YAML check [--format=FORMAT]

        checks if the urls in the yaml file exist

      bookmanager YAML urls  [--format=FORMAT]

        lists all urls of the yaml file

      bookmanager YAML list [--format=FORMAT]

        lists the yaml file


    Not implemented are the following features:

    1) pdf:  bookmanager pdf book.yml

    will be writing into the ./dist directory the output files with the names

    book.epub, book.pdf, and the dir html

  YAML Table of Contents format

    The table of contents for the book can be controled with a simple yaml file
    that has some specific contectual enhancements. THis include the creation of
    a BOOK section that has the sections outlined in hierarchical form, and
    contains chapter and section headers without links that are automatically
    generated.

    Here is an example of a simple TOC yaml file:

    * <https://github.com/cyberaide/bookmanager/blob/master/tests/python.yml>
```

## Refernces

* Example Yamle file: <https://github.com/cyberaide/bookmanager/blob/master/tests/python.yml>
* Home page: <https://github.com/cyberaide/bookmanager>
 
