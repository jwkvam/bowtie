FROM node:8.1.0

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
# let flit install packages as root
ENV FLIT_ROOT_INSTALL 1

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates

# miniconda archive
# https://repo.continuum.io/miniconda/
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.3.21-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

ENV PATH /opt/conda/bin:$PATH

RUN npm install -g webpack@2.6.1 yarn
RUN pip install flit

COPY . /bowtie
RUN cd /bowtie && flit install

WORKDIR /work

ENTRYPOINT [ "/usr/bin/tini", "--" ]
