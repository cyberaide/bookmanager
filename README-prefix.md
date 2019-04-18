
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

* Table of contents with indentation levels can be specified via Yaml
* Special variable substitution of elements defined in the yaml file
* Documts are fetched from github 
* The documents will be inspected and the images found in them are fetched 
  (we assume the images are relative to the document, http links will not be modified)
* Automatic generation of a cover page
* Output is generated in a dest directory

Planed enhancements:

* integration of Refernces via pandoc citeref
* integration of Section, Table, Image refernces via pandoc crossref

If you like to help get in contagt with Gregor von Laszewski
<laszewski@gmail.com>

```bash
$ pip install cyberaide-bookmanager
```

## Usage

