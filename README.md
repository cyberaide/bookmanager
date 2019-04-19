
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
produce the output. At present we only produce epubs, but it will be easy to
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
  bookmanager YAML pdf
  bookmanager YAML html
  bookmanager YAML docx
  bookmanager YAML check [--format=FORMAT]
  bookmanager YAML urls [--format=FORMAT]
  bookmanager YAML list [--format=FORMAT] [--details]


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

    The command searches for all images within the markdown document and fetches
    them so the document can be created locally with the images. We assume all
    images in the md document are for now not specified via http locations but
    via relative locations.

    To view the document use your favourite ePub Reader

    Other commands include:

      bookmanager YAML download [--format=FORMAT]

        downloads the urls into the ./dest directory for local processing

      bookmanager YAML check [--format=FORMAT]

        checks if the urls in the yaml file exist

      bookmanager YAML urls  [--format=FORMAT]

        lists all urls of the yaml file

      bookmanager YAML list [--format=FORMAT]

        lists the yaml file


    Not implemented are the following features:

    1) pdf:  bookmanager pdf book.yml

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

## Refernces

* Example Yamle file: <https://github.com/cyberaide/bookmanager/blob/master/tests/python.yml>
* Home page: <https://github.com/cyberaide/bookmanager>

## Requirements

Book manager requires the existence of some cloudmesh yaml files, In future releases we intend to remove them.
Simply do 

```bash
$ mkdir -p ~/.cloudmesh
$ wget -P ~/.cloudmesh https://raw.githubusercontent.com/cloudmesh/cloudmesh-cloud/master/cloudmesh/etc/cloudmesh4.yaml
$ wget -P ~/.cloudmesh https://raw.githubusercontent.com/cloudmesh/cloudmesh-common/master/cloudmesh/etc/cloudmesh.yaml
```

In addition we require an up to date version of pandoc. Please consult with the
pandoc documentation on how to do this. Unfortuantely the versions distributed
with ubuntu are outdated. On ubuntu you can say:

```bash
wget -q https://github.com/jgm/pandoc/releases/download/2.7.2/pandoc-2.7.2-1-amd64.deb
sudo dpkg -i pandoc-2.7.2-1-amd64.deb
pandoc --version
```
We recommend pandoc version 2.7.2.

## Example Yaml file

The following is an example for a table of contents yaml file that can be used
to pull together content from diferent repositories.

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
git:
  "book": "https://raw.githubusercontent.com/cloudmesh-community/book/master/chapters"
  "credit": "https://raw.githubusercontent.com/cyberaide/bookmanager/master/bookmanager/template"
BOOK:
  - PREFACE:
    - "{git.credit}/disclaimer.md"
  - INTRODUCTION:
    - "{git.book}/prg/SECTION-PYTHON.md"
    - "{git.book}/prg/python/python-intro.md"
    - "{git.book}/prg/python/python-install.md"
    - "{git.book}/prg/python/python-interactive.md"
    - "{git.book}/prg/python/python-editor.md"
    - "{git.book}/prg/python/python.md"
  - LIBRARIES:
    - "{git.book}/prg/python/python-libraries.md"
    - "{git.book}/prg/python/python-data.md"
    - "{git.book}/prg/python/python-matplotlib.md"
    - "{git.book}/prg/python/python-docopts.md"
    - "{git.book}/prg/python/python-cmd5.md"
    - "{git.book}/prg/python/python-cmd.md"
    - "{git.book}/prg/python/opencv/opencv.md"
    - "{git.book}/prg/python/opencv/secchi.md"
  - DATA:
    - "{git.book}/SECTION/SECTION-DATA.md"
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
```

