
# Bookmanager

[![Version](https://img.shields.io/pypi/v/cyberaide-bookmanager.svg)](https://pypi.python.org/pypi/cyberaide-bookmanager)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/cyberaide/bookmanager/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/cyberaide-bookmanager.svg)](https://pypi.python.org/pypi/cyberaide-bookmanager)
[![Format](https://img.shields.io/pypi/format/cyberaide-bookmanager.svg)](https://pypi.python.org/pypi/cyberaide-bookmanager)
[![Status](https://img.shields.io/pypi/status/cyberaide-bookmanager.svg)](https://pypi.python.org/pypi/cyberaide-bookmanager)
[![Travis](https://travis-ci.org/cyberaide/bookmanager.svg?branch=master)](https://travis-ci.org/cyberaide/bookmanager)




Bookmanager is a tool to create a publication from a number of sources on the
internet. It is especially useful to create customized books, lecture notes, or
handouts. Content is best integrated in markdown format as it is very fast to
produce the output. At present we only produce ePubs, but it will be easy to
also create pdf, html, work, odt and others. As we use pandoc we can support the
formats supported by it.

Implemented Features:

* Table of contents with indentation levels can be specified via yaml
* Special variable substitution of elements defined in the yaml file
* Documents are fetched from github 
* The documents will be inspected and the images found in them are fetched 
  (we assume the images are relative to the document, http links will not be modified)
* Automatic generation of a cover page
* Output is generated in a dest directory

Planed enhancements:

* integration of References via pandoc citeref
* integration of Section, Table, Image references via pandoc crossref

If you like to help get in contact with Gregor von Laszewski
<laszewski@gmail.com>

```bash
$ pip install cyberaide-bookmanager
```

## Usage


```
bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager version
  bookmanager YAML cover
  bookmanager YAML get [--format=FORMAT] [--force]
  bookmanager YAML download
  bookmanager YAML level
  bookmanager YAML epub [--force]
  bookmanager YAML pdf [--force]
  bookmanager YAML html
  bookmanager YAML docx
  bookmanager YAML check [--format=FORMAT]
  bookmanager YAML urls [--format=FORMAT]
  bookmanager YAML list [--format=FORMAT] [--details]
  bookmanager YAML pdfget [--force]

Arguments:
  YAML   the yaml file

Options:
  -h --help
  -f, --format=FORMAT     [default: markdown]
  -d, --details           [default: False]

Description:

    In principal you only need one command at this time. All other commands are
    available for test purposes.

    You can create an epub with

      bookmanager YAML get [--format=FORMAT]

        The command searches for all documents within the markdown document and
        fetches them so the document can be created locally. We assume all
        images in the md document are for now not specified via http locations
        but via relative locations. E.g. the images must be in an images folder
        next to the document.

        To view the document use your favourite ePub Reader

    Other commands include:

      bookmanager YAML download [--format=FORMAT]

        downloads the urls into the ./dest directory for local processing

      bookmanager YAML check [--format=FORMAT]

        checks if the urls in the yaml file exist

      bookmanager YAML urls  [--format=FORMAT]

        lists all urls of the yaml file

      bookmanager YAML list [--format=FORMAT] [--details]

        lists the yaml file

        If you specify as format list, you get presented with a list of dicts
        that can be used for further processing

        The list contains the attributes

          basename - the name of the md file without path
          counter - the counter in which the entry appears in the yaml file
          destination - the destination to which the file is copied
          dirname - the path without the basename
          format - the format (md for markdown)
          indent - a default indent that is used for easy printing in hierarchical format
          kind - section or header (a section is a document)
          level - the level this entry occurs
          name - if its a section it defines the section name
          path - the parent path
          prefix - the file prefix (http* or file*)
          title - this is tha basename (we need to add a new mdtitle)
          topic - not used so far
          uri - the location wheer to find the file


    Not implemented are the following features:

    bookmanager YAML pdfget [--force]

        The command searches for all documents within the markdown document and
        fetches them so the document can be created locally. In contrast to the
        get command this command only takes PDF documents as input. The output
        will be a PDF document only.

    YAML Table of Contents format:

      The table of contents for the book can be controlled with a simple yaml
      file that has some specific contextual enhancements. THis include the
      creation of a BOOK section that has the sections outlined in hierarchical
      form, and contains chapter and section headers without links that are
      automatically generated.

    Here is an example of a simple TOC yaml file:

    * https://github.com/cyberaide/bookmanager/blob/master/tests/python.yml

    Bugs and enhancement suggestions:

    * https://github.com/cyberaide/bookmanager/issues
```

## Cover Page 

Book manager can create a simple cover page for you.

and example is given at 


* <https://github.com/cyberaide/bookmanager/blob/master/tests/exmaple/cover.png>

![Cover Page](https://github.com/cyberaide/bookmanager/raw/master/tests/exmaple/cover-thumb.png)


## Example creation

```bash
$ git clone https://github.com/cyberaide/bookmanager.git
$ cd bookmanager
$ pip install -e .
$ bookmanager tests/python.yaml get
$ open dest/book.epub
```

## References

* Example Yaml file: <https://github.com/cyberaide/bookmanager/blob/master/tests/python.yml>
* Home page: <https://github.com/cyberaide/bookmanager>

## Requirements

Book manager requires the existence of some cloudmesh yaml files, In future releases we intend to remove them.
Simply do 

```bash
$ mkdir -p ~/.cloudmesh
$ wget -P ~/.cloudmesh https://raw.githubusercontent.com/cloudmesh/cloudmesh-configuration/master/cloudmesh/configuration/etc/cloudmesh.yaml
```

In addition we require an up to date version of pandoc. Please consult with the
pandoc documentation on how to do this. Unfortunately the versions distributed
with ubuntu are outdated. On ubuntu you can say:

```bash
wget -q https://github.com/jgm/pandoc/releases/download/2.7.2/pandoc-2.7.2-1-amd64.deb
sudo dpkg -i pandoc-2.7.2-1-amd64.deb
pandoc --version
```

We recommend a very new version of pandoc and pandoc-crossref. Look in
our Dockerfile to see how you can install them from source.

## Bookmanager Service

A graphical user interface for selecting chapters and changing their order is available at 

* <https://github.com/cyberaide/bookmanager-service/blob/master/README.md>


## Example Yaml file

The following is an example for a table of contents yaml file that can be used
to pull together content from different repositories.

```
---
metadata:
  image: "cover.png"
  title: "Introduction to Python"
  subtitle: "for Cloud Computing"
  author: 'Gregor von Laszewski'
  subauthor: "Editor"
  email: "laszewski@gmail.com"
  url: "https://github.com/cyberaide/bookmanager"
  description: "Book creator"
  abstract: "my abstract"
  keywords: "pandoc"
  stylesheet: "epub.css"
  dest: "./dest/book"
  filename: "vonLaszewski-python.epub"
  rights: (c) Gregor von Laszewski, 2018, 2019
git:
  "book": "https://raw.githubusercontent.com/cloudmesh-community/book/master/chapters"
  "bookmanager": "https://raw.githubusercontent.com/cyberaide/bookmanager/master/bookmanager/template"
BOOK:
  - PREFACE:
      - "{git.bookmanager}/disclaimer.md"
  - INTRODUCTION:
    - "{git.book}/prg/python/python-intro.md"
  - INSTALATION:
      - "{git.book}/prg/python/python-install.md"
      - "{git.book}/prg/python/python-install-pyenv.md"
  - FIRST_STEPS:
      - "{git.book}/prg/python/python-interactive.md"
      - "{git.book}/prg/python/python-editor.md"
  - LANGUAGE:
      - "{git.book}/prg/python/python.md"
  - CLOUDMESH_COMMON:
      - "{git.book}/prg/python/cloudmesh/console.md"
      - "{git.book}/prg/python/cloudmesh/dict.md"
      - "{git.book}/prg/python/cloudmesh/shell.md"
      - "{git.book}/prg/python/cloudmesh/stopwatch.md"
  - LIBRARIES:
    - "{git.book}/prg/python/python-libraries.md"
    - "{git.book}/prg/python/python-data.md"
    - "{git.book}/prg/python/python-matplotlib.md"
    - "{git.book}/prg/python/python-docopts.md"
    - "{git.book}/prg/python/cloudmesh/python-cmd5.md"
    - "{git.book}/prg/python/python-cmd.md"
    - "{git.book}/prg/python/opencv/opencv.md"
    - "{git.book}/prg/python/opencv/secchi.md"
  - DATA:
    - "{git.book}/data/formats.md"
  - MONGO:
    - "{git.book}/data/mongodb.md"
    - "{git.book}/data/mongoengine.md"
  - OTHER:
    - "{git.book}/prg/python/python-wordcount.md"
    - "{git.book}/prg/python/numpy/numpy.md"
    - "{git.book}/prg/python/scipy/scipy.md"
    - "{git.book}/prg/python/scikit-learn/scikit-learn.md"
    - "{git.book}/prg/python/random-forest/random-forest.md"
    - "{git.book}/prg/python/python-parallel.md"
    - "{git.book}/prg/python/dask/dask.md"
  - APPLICATIONS:
    - "{git.book}/prg/python/fingerprint/fingerprint.md"
    - "{git.book}/prg/python/facedetection/facedetection.md"
  - REFERENCES:
      - "{git.bookmanager}/empty.md"
```

## Alternative Instalations

The pip install requires that you have pandoc and pandoc-citeref
installed. A NAtive install with pip has the advantage that it may be
much faster than for example an instalation in a virtual machine via
vagrant or a container.

However, these instalation methods may be much easier as you do not have
toinstall that dependencies yourself.

### Instalation in a Container

The image for bookmanager is available at 

* <https://hub.docker.com/repository/docker/cloudmesh/bookmanager>

To pull the premade image please use

```
docker pull cloudmesh/bookmanager:latest
```

Now you can list the images with 

```
docker image list
```

to run a shell in a container that includes bookmanager, please use 

```bash
docker run -v `pwd`:/cm -w /cm --rm -it cloudmesh/bookmanager:0.2.30  /bin/bash
```

In that shell you can call `bookmanager`

### Instalation for Developers on macOS and Linux

See the next section and execute the commands we give in the Makefile
targets while completing the variables accordingly. You can also install
make via choco and use the Makefile.

We ar looking a Windows user that can contribute a bat file or a
packaged .exe, or give us the example command for docker

### Instalation for Developers on macOS and Linux
 

Here the preparation steps:

 
```bash
mkdir cm
cd cm
git clone https://github.com/cyberaide/bookmanager.git
cd bookmanager
make image
```

Now you can use that image to create books. We will explain here a more advanced example



TODO: give an example here while compiling our cloud computing book

```bash cd cm mkdir cm/pub git clone
https://github.com/cloudmesh-community/book.git make cm 
``` 

This will log you into the container that alsoo has the cm volume
mounted in /cm now you can use the bookmanager in cm while using the
content that you have in your native OS.
 
In the container you need to do the following:

 
```bash
/cm# cd book
/cm/book# cd books/cd 516-sp20/
:/cm/book/books/516-sp20# time make proceedings
```
 

The output is in `/cm/pub/docs` in teh container or the `pub` folder on
your native OS that you previously created.

To show you the performance differences on this more complex example I
copied some information from my computer:
  

| Mode | time on Gregor's macOS |
| ------ | ------ |
| Native | 34.948s |
| Container with mount of cm in host system | 48.782s |
| Container with locally checked out book folder | 40.372s |
