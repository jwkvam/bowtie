Using Docker
============

Bowtie depends on `yarn <https://yarnpkg.com/>`_ to manage Node packages.
If you would prefer to not install this on your system you
can use the provided Dockerfile to build your Bowtie app.
The file provides a conda environment with python 3.6.

Docker Hub
----------

The Docker image is hosted on `Docker Hub` <https://hub.docker.com/r/jwkvam/bowtie/>`__.
To pull the bleeding edge release::

    docker pull jwkvam/bowtie

To pull a specific version::

    docker pull jwkvam/bowtie:0.6.0

Building
--------

If you prefer to build the Docker yourself::

    docker build . -t bowtie

Usage
-----

I recommend running the Docker interactively::

    docker run -ti -p 9991:9991 -v (pwd):/work -rm bowtie bash

This runs Docker in your current working directory.
Run this command in the same directory as your bowtie project.
This forwards the Docker port 9991 to the host,
so you can access the dashboard from the host machine.

You may find it convenient to make this command an alias::

    alias bowtie='docker run -ti -p 9991:9991 -v (pwd):/work -rm bowtie bash'

Let's say your dashboard is in ``app.py`` and you have a ``requirements.txt`` file::

    $ bowtie
    # now inside the docker
    bowtie $ pip install -r requirements.txt
    bowtie $ python app.py run

After a few moments you should be able to access the website from your machine.
