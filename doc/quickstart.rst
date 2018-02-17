.. Bowtie documentation master file, created by
   sphinx-quickstart on Fri Aug 19 23:07:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _quickstart:

Quick Start
===========

This quick start will show how to do the following:

* Install everything needed to use Bowtie.
* Write an app connecting a slider to a plot.
* How to deploy to Heroku.

Install Bowtie
--------------

If you use ``conda``, you can install with::

    conda install -c conda-forge bowtie-py

If you use ``pip``, you can install with::

    pip install bowtie

To install bleeding edge you can use `flit <http://flit.readthedocs.io/en/latest/index.html>`_, to install::

    flit install

Install Yarn
------------

Bowtie uses `Yarn <https://yarnpkg.com/>`_ to manage the Javascript libraries
We need to install it before we can use Bowtie.
If you installed Bowtie with ``conda``, Yarn was installed as a dependency and you can move on to `Creating Your First App`_.

Conda Install
^^^^^^^^^^^^^

Yarn is available through conda-forge::

    conda install -c conda-forge yarn

MacOS Install
^^^^^^^^^^^^^

Yarn is available through Homebrew::

    brew install yarn

Other Environments
^^^^^^^^^^^^^^^^^^

For other environments please follow the `install instructions <https://yarnpkg.com/en/docs/install>`_
on the official website.


Creating Your First App
-----------------------

First we'll import the components we plan on using::

    from bowtie.visual import Plotly
    from bowtie.control import Nouislider
    import numpy as np
    import plotlywrapper as pw

I imported `Plotlywrapper <https://github.com/jwkvam/plotlywrapper>`_ and `Numpy <http://www.numpy.org/>`_
to make the generation of `Plotly <https://plot.ly/>`_ plots easier.
Now we instantiate the components and configure them::

    sine_plot = Plotly()
    freq_slider = Nouislider(caption='frequency', minimum=1, maximum=10, start=5)

Next we'll create a listener that generates a plot on slider changes::

    def listener(freq):
        freq = float(freq[0])
        t = np.linspace(0, 10, 100)
        sine_plot.do_all(pw.line(t, np.sin(freq * t)).to_json())

If you prefer not to use ``plotlywrapper``::

    def listener(freq):
        freq = float(freq[0])
        t = np.linspace(0, 10, 100)
        sine_plot.do_all({
            'data': [{
                'type': 'scatter',
                'mode': 'lines+markers',
                'x': t,
                'y': np.sin(freq * t)
            }]
        })

The :py:class:`bowtie.control.Nouislider` component sends its values as a list of strings so we had to cast it to a float.

Lastly we need to build the application by laying out the components and connecting listeners to events.
The ``App`` class handles this and we put this logic into a function.
Bowtie provides a decorator, ``command``, which we'll use to make a simple command line interface.
To finish, we simply wrap the function with the ``command`` decorator::

    from bowtie import command
    @command
    def main():
        from bowtie import App
        app = App()
        app.add_sidebar(freq_slider)
        app.add(sine_plot)
        app.subscribe(listener, freq_slider.on_change)
        return app

Now take a look at the CLI we just created by running this script::

    python app.py

The output should look something like this::

    Usage: app.py [--help] COMMAND [ARGS]...

      Bowtie CLI to help build and run your app.

    Options:
      --help  Show this message and exit.

    Commands:
      build  Writes the app, downloads the packages, and...
      dev    Recompiles the app for development.
      prod   Recompiles the app for production.
      run    Build the app and serve it.
      serve  Serves the Bowtie app locally.

To construct the app, we run the script with the ``build`` command::

    python app.py build

This will construct the app, install the JavaScript libraries and compile your project.
Once it's done you should be able to run the following to launch your app::

    python app.py serve

That will launch the app locally and you should be able to access it at http://localhost:9991.

Deploy to Heroku
----------------

This isn't streamlined right now but you can try the following approach.
For example, this was done to create `bowtie-demo <https://github.com/jwkvam/bowtie-demo/>`_ so you may refer to that.

* Create the Procfile, try the following::

    web: python app.py serve -p $PORT

* Create requirements files, again see `bowtie-demo <https://github.com/jwkvam/bowtie-demo/>`_ for an example.
* Rebuild with production settings with webpack, by default Bowtie makes a development build::

    python app.py prod

* Commit the following files to your repo::

    build/src/server.py
    build/src/templates/index.html
    build/src/static/bundle.js.gz

* Finally push your repo to Heroku!
