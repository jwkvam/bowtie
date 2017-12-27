.. Bowtie documentation master file, created by
   sphinx-quickstart on Fri Aug 19 23:07:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

App
===

The App class defines the structure of the application.
It contains a root view, what you get when you go to '/'.
It subscribes functions to component events and builds the application.

.. autoclass:: bowtie.App
    :members:
    :undoc-members:

View
----

Views are responsible for laying components out on a webpage.
Each view defines a grid and optional sidebar.
Each app comes with one root view and you can add as many additional routes and view as you want.

.. autoclass:: bowtie.View
    :members:
    :undoc-members:

Size
----

Each row and column in the app is a ``Size`` object.
The space used by each row and column can be changed through the following methods.

.. autoclass:: bowtie._app.Size
    :members:
    :undoc-members:

Gap
---

Set the margin between the cells of the grid in the App.

.. autoclass:: bowtie._app.Gap
    :members:
    :undoc-members:
