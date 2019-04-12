
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
```
bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager url download YAML [--format=FORMAT]
  bookmanager url check YAML [--format=FORMAT]
  bookmanager url list YAML [--format=FORMAT]
  bookmanager list YAML [--format=FORMAT]
  bookmanager epub YAML
  bookmanager info


Arguments:
  YAML   the yaml file

Options:
  -h --help
  -f, --format=FORMAT     [default: markdown]

Description:

  bookmanager url download YAML [--format=FORMAT]

    downloads the urls into the ./dist directory for local processing

  bookmanager url check YAML [--format=FORMAT]

    checks if the urls in the yaml file exist

  bookmanager url list YAML [--format=FORMAT]

    lists all urls of the yaml file

  bookmanager list YAML [--format=FORMAT]

    lists the yaml file

  Creation of a book:

    1) create a yaml file book.yml
    2) check:    bookmanager url check book.yml
    3) download: bookmanager download check book.yml

    NOt implemented yet the output

    4} epub: bookmanager epub book.yml
    5) html: bookmanager html book.yml
    6) pdf:  bookmanager pdf book.yml

    will be written into the ./dist directory with the names

    book.epup, book.pdf, and the dir html
```
