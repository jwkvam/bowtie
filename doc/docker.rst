Using Docker
============

Bowtie depends on
`yarn <https://yarnpkg.com/>`_
and
`webpack <https://webpack.js.org/>`_
which are tools from the Node ecosystem.
If you would prefer to not install these on your system you
can use the provided Dockerfile to build your Bowtie app.
The file provides a conda environment with python 3.6.

Building
--------

I don't host a docker image anywhere so you'll need to build it yourself for now::

    docker build . -t bowtie

Then I recommend running it in detached mode so we can give it multiple commands.
We also share your working directory so you can use the built files::

    docker run --name bt -v /your/apps/path:/work -d bowtie

Now you can install any pip or conda requirements::

    docker exec bt conda install --file conda-requirements.txt
    docker exec bt pip install -r requirements.txt

Then finally build your app::

    docker exec bt ./app.py build

Upon completion you should be able to run the app locally.
