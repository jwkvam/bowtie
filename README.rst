`Installation`_ |
`Documentation <https://bowtie-py.readthedocs.io/en/stable>`__ |
`Gitter Chat <https://gitter.im/bowtie-py/Lobby>`__ |
`Google Group <https://groups.google.com/forum/#!forum/bowtie-py>`__

======
Bowtie
======

|Build Status| |Documentation Status| |PyPI version| |Conda version| |PyPI| |codecov|

.. figure:: https://cloud.githubusercontent.com/assets/86304/20045988/69e5678a-a45a-11e6-853b-7f60a615c9da.gif
   :alt: Demo

Introduction
------------

Bowtie is a library for writing dashboards in Python. No need to know
web frameworks or JavaScript, focus on building functionality in Python.
Interactively explore your data in new ways! Deploy and share with
others!

Demo
----

See a live `example <https://bowtie-demo.herokuapp.com/>`__ generated
from this
`code <https://github.com/jwkvam/bowtie-demo/blob/master/example.py>`__!

Gallery
-------

For more examples, check out the
`gallery <https://github.com/jwkvam/bowtie/wiki/Gallery>`__. Feel free
to add your own creations!

Installation
------------

If you use ``conda``, you can install with::

    conda install -c conda-forge bowtie-py

If you use ``pip``, you can install with::

    pip install bowtie

Requirements
^^^^^^^^^^^^

Bowtie uses `Yarn <https://yarnpkg.com>`__ to manage node packages.
If you installed Bowtie through ``conda``, Yarn was also installed as a dependency.
Yarn can be installed through conda::

    conda install -c conda-forge yarn

Otherwise follow `install
instructions <https://yarnpkg.com/en/docs/install>`__ for Yarn for your
OS.

Documentation
-------------

Available `here <https://bowtie-py.readthedocs.io/en/latest/>`__.

Docker
------

Docker images are provided as an alternative way to use Bowtie. They are
available on `Docker Hub <https://hub.docker.com/r/jwkvam/bowtie/>`__::

    docker pull jwkvam/bowtie

Read the
`documentation <https://bowtie-py.readthedocs.io/en/latest/docker.html>`__
for more details.

The Goal
--------

.. figure:: https://cloud.githubusercontent.com/assets/86304/18606859/8ced55a6-7c70-11e6-8b5e-fba0ffcd78da.png
      :alt: @astrobiased @treycausey @vagabondjack the lack of a comprehensive production-grade Shiny-alike for Python is a Big Problem

Contributing
------------

You can help Bowtie in many ways including:

- Try it `out <http://bowtie-py.readthedocs.io/en/latest/quickstart.html>`__ and report bugs or what was difficult.
- Help improve the `documentation <https://github.com/jwkvam/bowtie/tree/master/doc>`__.
- Write new `widgets <http://bowtie-py.readthedocs.io/en/latest/newcomponents.html>`__.
- Provide hosting for apps in the gallery.
- Say `thanks <https://saythanks.io/to/jwkvam>`__!

.. |Join the chat at https://gitter.im/bowtie-py/Lobby| image:: https://badges.gitter.im/bowtie-py/Lobby.svg
   :target: https://gitter.im/bowtie-py/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |Forum| image:: https://img.shields.io/badge/-Google%20Group-blue.svg
   :target: https://groups.google.com/forum/#!forum/bowtie-py
.. |Documentation Status| image:: https://readthedocs.org/projects/bowtie-py/badge/?version=latest
   :target: http://bowtie-py.readthedocs.io/en/latest/?badge=latest
.. |Build Status| image:: https://travis-ci.org/jwkvam/bowtie.svg?branch=master
   :target: https://travis-ci.org/jwkvam/bowtie
.. |PyPI version| image:: https://badge.fury.io/py/bowtie.svg
   :target: https://badge.fury.io/py/bowtie
.. |Conda version| image:: https://anaconda.org/conda-forge/bowtie-py/badges/version.svg   
   :target: https://anaconda.org/conda-forge/bowtie-py
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/bowtie.svg
   :target: https://pypi.python.org/pypi/bowtie/
.. |codecov| image:: https://codecov.io/gh/jwkvam/bowtie/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jwkvam/bowtie
