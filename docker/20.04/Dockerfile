#
# UBUNTU 20.04
#
FROM ubuntu:20.04
MAINTAINER Gregor von Laszewski <laszewski@gmail.com>


ENV DEBIAN_FRONTEND noninteractive

#
# UPDATE THE SYSTEM
#
RUN apt-get -y update
RUN apt-get -y dist-upgrade
RUN apt-get install -y --no-install-recommends apt-utils

#
# SYSTEM TOOLS
#
RUN apt-get install -y \
    git \
    git-core \
    wget \
    curl \
    rsync \
    emacs-nox

#
# DEVELOPMENT TOOLS
#
RUN apt-get install -y build-essential checkinstall --fix-missing
RUN apt-get install -y \
    lsb-core \
    dnsutils \
    libssl-dev \
    libffi-dev \
    libreadline-gplv2-dev \
    libncursesw5-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
    libffi-dev \
    zlib1g-dev

#
# GRAPHICS
#
RUN apt-get install -y graphviz

# Install LaTeX

RUN apt-get -y install texlive
RUN ln -snf /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install texlive-latex-extra
RUN apt-get -y install texlive-fonts-recommended texlive-fonts-extra
RUN unset DEBIAN_FRONTEND
RUN apt-get -y install biber

#
# INSTALL PYTHON 3.9 FROM SOURCE
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

#
# Pandoc extensions
#
RUN pip install pandoc-include
RUN pip install pandoc-xnos

#
# BOOKMANAGER
#
RUN git clone https://github.com/cyberaide/bookmanager.git

WORKDIR /usr/local/code/bookmanager


RUN pip install -e .

#
# CHECK
#
RUN python --version
RUN pip install -U pip
RUN pip --version
RUN pandoc --version

WORKDIR /root

#ENTRYPOINT ["/bookmanager/bin/pull.sh"]

CMD [ "/bin/bash" ]



