.. Bowtie documentation master file, created by
   sphinx-quickstart on Fri Aug 19 23:07:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bowtie: Interactive Dashboard Toolkit
=====================================

Bowtie helps you visualize your data interactively.
No Javascript required, you build your dashboard in pure Python.
Easy to deploy so you can share results with others.

New to Bowtie?
The :ref:`quickstart guide <quickstart>` will get you running your first app.
It takes about 10 minutes to go through.

Notable Features
----------------

* Ships with many useful widgets including charts, tables, dropdown menus, sliders, and markdown.
* All widgets come equipped with events and commands for interaction.
* Hook into Plotly charts with click, selection, and hover events.
* Jupyter integration allows you to prototype your dashboards.
* Schedule functions to run on a timer.
* Store and fetch data with the client (browser).
* Built in progress indicators for all visual widgets.
* Powerful Pythonic grid API to layout components, **not** in HTML and CSS.
* Compiles a single Javascript bundle speeding up load times and removes CDN dependencies.
* Powerful programming model let's you listen to multiple events and update multiple widgets with single functions.

.. * Facebook's React ecosystem gives access to many high quality widgets
.. * One self-contained package includes all Python and Javascript

Contents
--------

.. toctree::
    :maxdepth: 2
    :caption: Getting Started

    quickstart

.. toctree::
    :maxdepth: 2
    :caption: User Guide

    app
    components
    feedback
    cache
    authentication
    flask
    deploy
    jupyter
    docker
    exceptions

.. toctree::
    :maxdepth: 2
    :caption: Developer Guide

    architecture
    newcomponents

.. toctree::
    :maxdepth: 2
    :caption: Miscellaneous

    comparison
    indices
