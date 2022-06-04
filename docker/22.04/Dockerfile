#
# UBUNTU 22.04
#
FROM ubuntu:22.04
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
    libreadline-dev \
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
ENV PYTHON_VERSION=3.10.4

RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
RUN tar xzf Python-${PYTHON_VERSION}.tgz
WORKDIR /usr/src/Python-${PYTHON_VERSION}
RUN ./configure --enable-optimizations
RUN make altinstall
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.10 10
RUN update-alternatives --config python
RUN update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.10 10
RUN update-alternatives --config pip
RUN yes '' | update-alternatives --force --all
ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /usr/local/code


#
# INSTALL PANDOC
#
# https://github.com/jgm/pandoc/releases/download/2.18/pandoc-2.18-1-amd64.deb

ENV PANDOC_MAJOR="2.18"
ENV PANDOC_MINOR="-1"
ENV PANDOC_VERSION="$PANDOC_MAJOR$PANDOC_MINOR"

RUN echo $PANDOC_VERSION
RUN wget -q https://github.com/jgm/pandoc/releases/download/${PANDOC_MAJOR}/pandoc-${PANDOC_VERSION}-amd64.deb
RUN dpkg -i pandoc-${PANDOC_VERSION}-amd64.deb

# INSTALL STACK FOR CROSSREF  \

RUN wget -qO- https://get.haskellstack.org/ | sh

# CROSSREFF FROM SOURCE
# https://github.com/lierdakil/pandoc-crossref/archive/refs/tags/v0.3.13.0.tar.gz
# ENV CROSSREF_VERSION=v0.3.13.0
RUN git clone https://github.com/lierdakil/pandoc-crossref.git

WORKDIR /usr/local/code/pandoc-crossref

RUN mkdir -p /root/.local/bin
RUN stack install
RUN cp /root/.local/bin/pandoc-crossref /usr/local/bin

# https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.12.0c/pandoc-crossref-Linux.tar.xz
#ENV CROSSREF_VERSION=v0.3.13.0
#RUN wget https://github.com/lierdakil/pandoc-crossref/releases/download/${CROSSREF_VERSION}/pandoc-crossref-Linux.tar.xz
#RUN tar xvf pandoc-crossref-Linux.tar.xz

#
# Pandoc extensions
#
RUN pip install pandoc-include
RUN pip install pandoc-xnos

RUN pip install pip -U
#
# BOOKMANAGER
#
WORKDIR /usr/local/code

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
RUN pandoc-crossref --numeric-version

WORKDIR /root

#ENTRYPOINT ["/bookmanager/bin/pull.sh"]

CMD [ "/bin/bash" ]



