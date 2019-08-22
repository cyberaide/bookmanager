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
We recommend pandoc version 2.7.2.

## Example Yaml file

The following is an example for a table of contents yaml file that can be used
to pull together content from different repositories.
