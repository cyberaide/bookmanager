#
# UBUNTU 20.04
#
FROM ubuntu:20.04

MAINTAINER Gregor von Laszewski <laszewski@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

#
# UPDATE THE SYSTEM
#
RUN apt-get -y update --fix-missing
RUN apt-get -y dist-upgrade
RUN apt-get install -y --no-install-recommends apt-utils

#
# DEVELOPMENT TOOLS
#
RUN apt-get install -y build-essential checkinstall --fix-missing
RUN apt-get install -y lsb-core
RUN apt-get install -y dnsutils
RUN apt-get install -y libssl-dev
RUN apt-get install -y libffi-dev
RUN apt-get install -y libreadline-gplv2-dev
RUN apt-get install -y libncursesw5-dev
RUN apt-get install -y libsqlite3-dev
RUN apt-get install -y libgdbm-dev
RUN apt-get install -y libc6-dev
RUN apt-get install -y libbz2-dev
RUN apt-get install -y libffi-dev
RUN apt-get install -y zlib1g-dev

RUN apt-get install -y git-core
RUN apt-get install -y git

RUN apt-get install -y wget
RUN apt-get install -y curl
RUN apt-get install -y rsync

RUN apt-get install -y graphviz


#
# install
#
RUN apt-get install -y emacs-nox
RUN apt-get -y install biber

#RUN yes | pacman -Sy lsb-release



#
# INSTALL PYTHON 3.8 FROM SOURCE
#

WORKDIR /usr/src

ENV PYTHON_VERSION=3.9.7

RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
RUN tar xzf Python-${PYTHON_VERSION}.tgz

WORKDIR /usr/src/Python-${PYTHON_VERSION}

RUN ./configure --enable-optimizations

RUN make altinstall

RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.9 10
RUN update-alternatives --config python

RUN update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.9 10
RUN update-alternatives --config pip

RUN yes '' | update-alternatives --force --all


ENV PATH="/usr/local/bin:${PATH}"

RUN python3.9 --version
RUN python --version
RUN pip install -U pip
RUN pip --version



WORKDIR /usr/local/code

#
# INSTALL PANDOC
#
# https://github.com/jgm/pandoc/releases/download/2.14.2/pandoc-2.14.2-1-amd64.deb
ENV PANDOC_VERSION=2.14.2
RUN wget -q https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/pandoc-${PANDOC_VERSION}-1-amd64.deb
RUN dpkg -i pandoc-${PANDOC_VERSION}-1-amd64.deb
RUN pandoc --version

# https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.12.0c/pandoc-crossref-Linux.tar.xz
ENV CROSSREF_VERSION=v0.3.12.0c
RUN wget https://github.com/lierdakil/pandoc-crossref/releases/download/${CROSSREF_VERSION}/pandoc-crossref-Linux.tar.xz
RUN tar xvf pandoc-crossref-Linux.tar.xz

RUN mv pandoc-crossref /usr/local/bin


RUN git clone https://github.com/cyberaide/bookmanager.git

WORKDIR /usr/local/code/bookmanager


RUN pip install -e .

WORKDIR /root

#ENTRYPOINT ["/bookmanager/bin/pull.sh"]

CMD [ "/bin/bash" ]



