FROM node:8.9

LABEL maintainer="jwkvam@gmail.com"

ENV FLIT_ROOT_INSTALL 1
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends curl bzip2 ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# miniconda archive
# https://repo.continuum.io/miniconda/
RUN echo "export PATH=/opt/conda/bin:$PATH" > /etc/profile.d/conda.sh && \
    curl -L https://repo.continuum.io/miniconda/Miniconda3-4.3.30-Linux-x86_64.sh -o ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

ENV PATH /opt/conda/bin:$PATH

RUN npm install -g webpack@3.8.1 yarn
RUN pip install flit

WORKDIR /bowtie
COPY . /bowtie
RUN flit install
WORKDIR /work

ENTRYPOINT [ "sleep", "infinity" ]
