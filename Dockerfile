#
# UBUNTU 19.10
#
FROM ubuntu:19.10

MAINTAINER Gregor von Laszewski <laszewski@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

#
# UPDATE THE SYSTEM
#
RUN apt-get -y update
RUN apt-get -y dist-upgrade
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get update --fix-missing

#
# DEVELOPMENT TOOLS
#
RUN apt-get install -y graphviz
RUN apt-get install -y wget
RUN apt-get install -y curl
RUN apt-get install -y rsync
RUN apt-get install -y git-core
RUN apt-get install -y dnsutils
RUN apt-get install -y build-essential checkinstall
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
RUN apt-get install -y git
RUN apt-get install -y lsb-core

#
# install
#
RUN apt-get install -y emacs-nox
RUN apt-get -y install biber

#RUN yes | pacman -Sy biber
#RUN yes | pacman -Sy emacs
#RUN yes | pacman -Sy lsb-release



#
# INSTALL PYTHON 3.8 FROM SOURCE
#

WORKDIR /usr/src

RUN wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz
RUN tar xzf Python-3.8.2.tgz

WORKDIR /usr/src/Python-3.8.2

RUN ./configure --enable-optimizations

RUN make altinstall


#
# INSTALL PACKAGED PYTHON 3.8
#

#RUN apt-get install -y software-properties-common
#RUN add-apt-repository ppa:ubuntu-toolchain-r/ppa
# RUN pip install --upgrade pip setuptools

#RUN apt-get autoremove

#RUN apt-get install -y python3.8
# RUN apt-get install python3-distutils
# RUN apt-get install python3-setuptools
# RUN sudo easy_install3 pip
#RUN apt-get install -y python3-pip
#RUN pip3 install --upgrade pip setuptools


RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.8 10
RUN update-alternatives --config python

RUN update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.8 10
RUN update-alternatives --config pip

RUN yes '' | update-alternatives --force --all


ENV PATH="/usr/local/bin:${PATH}"

RUN python3.8 --version
RUN python --version
RUN pip install -U pip
RUN pip --version



WORKDIR /tmp

#
# INSTALL PANDOC
#           
RUN wget -q https://github.com/jgm/pandoc/releases/download/2.9.1.1/pandoc-2.9.1.1-1-amd64.deb
RUN dpkg -i pandoc-2.9.1.1-1-amd64.deb
RUN pandoc --version

RUN wget https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.6.1b/linux-pandoc_2_9_1_1.tar.gz
RUN tar xvf linux-pandoc_2_9_1_1.tar.gz

RUN mv pandoc-crossref /usr/local/bin


RUN git clone https://github.com/cyberaide/bookmanager.git

WORKDIR /tmp/bookmanager


RUN pip install -e .

WORKDIR /root

#ENTRYPOINT ["/bookmanager/bin/pull.sh"]

CMD [ "/bin/bash" ]



