.. Bowtie documentation master file, created by
   sphinx-quickstart on Fri Aug 19 23:07:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Layout
======

The Layout class defines the structure of the application:
how things are laid out, subscribing listeners to events, and building the application.

.. autoclass:: bowtie.Layout
    :members:
    :undoc-members:

Each row and column in the layout is a ``Size`` object.
The space used by each row and column can be changed through the following methods.

.. autoclass:: bowtie._layout.Size
    :members:
    :undoc-members:
