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

:/cm/book/books/516-sp20# ls -1

Makefile

aa.yaml

dest

e516-datacenter.yaml

e516-draft.yaml

e516-sp20-proceedings.yaml

e516-sp20-proceedings.yaml.bak

e516-sp20-syllabus.yaml

e516-sp20.yaml

e516.yaml

reports.md

:/cm/book/books/516-sp20# time make proceedings
```
 

The output is in `/cm/pub/docs` in teh container or the `pub` folder on
your native OS that you previously created.

To show you the performance differences I copied some information from
my computer:
  

Native:

```
real 0m34.948s
user 0m13.971s
sys 0m2.680s
```
 
Container with mount of cm in host system e.g. osx:
 
```
real 0m48.782s
user 0m16.872s
sys 0m2.428s
```
 
Container with locally checked out books folder

```
real 0m40.372s
user 0m13.606s
sys 0m1.670s
```
