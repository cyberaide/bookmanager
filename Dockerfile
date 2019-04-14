#
# USE ARCHLINUX
#
FROM ubuntu:18.04

MAINTAINER Gregor von Laszewski <laszewski@gmail.com>


RUN apt-get update --fix-missing


#
# DEVELOPMENT TOOLS
#
RUN apt-get update -y
RUN apt-get install graphviz -y
RUN apt-get install python-pip -y
RUN apt-get install wget -y
RUN apt-get install curl -y
RUN apt-get install rsync -y
RUN pip install pip -U
RUN apt-get install git-core -y
RUN apt-get install dnsutils -y
RUN apt-get install -y build-essential libssl-dev libffi-dev

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/ppa


#
# INSTALL PYTHON 3.7.2
#

RUN pip install --upgrade pip setuptools
RUN apt-get install -y python3.7
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip setuptools


RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 10
RUN update-alternatives --config python

RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10
RUN update-alternatives --config pip

RUN yes '' | update-alternatives --force --all

RUN python3 --version
RUN python --version
RUN pip --version

#
# INSTALL PANDOC
#
RUN wget -q https://github.com/jgm/pandoc/releases/download/2.7.2/pandoc-2.7.2-1-amd64.deb
RUN dpkg -i pandoc-2.7.2-1-amd64.deb
RUN pandoc --version


RUN git clone https://github.com/cyberaide/bookmanager.git

RUN mkdir -p ~/.cloudmesh
RUN wget -P ~/.cloudmesh https://raw.githubusercontent.com/cloudmesh/cloudmesh-cloud/master/cloudmesh/etc/cloudmesh4.yaml
RUN wget -P ~/.cloudmesh https://raw.githubusercontent.com/cloudmesh/cloudmesh-common/master/cloudmesh/etc/cloudmesh.yaml

WORKDIR bookmanager

RUN pip install -e .

CMD ["git", "pull"]

CMD [ "/bin/bash" ]
