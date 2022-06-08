## Cover Page 

Book manager can create a simple cover page for you. An example is given at 

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

* Example YAML file: <https://github.com/cyberaide/bookmanager/blob/master/tests/python.yml>
* Home page: <https://github.com/cyberaide/bookmanager>

## Requirements

We require 

* pandoc (2.18)
* pandoc-citeproc (installed from source via stack install)
* LaTeX such as texlive full
* an epub reader such as calibre on Windows or Linux

To se how to install it, look in our Dockerfile and adapt for your local install

## Bookmanager Service

A graphical user interface for selecting chapters and changing their order is available at 

* <https://github.com/cyberaide/bookmanager-service/blob/master/README.md>

However this has not been updated for a while and may likely not work.

## Example YAML file

The following is an example for a table of contents yaml file that can be used
to pull together content from different repositories.
