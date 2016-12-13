.. Bowtie documentation master file, created by
   sphinx-quickstart on Fri Aug 19 23:07:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Quick Start
===========

This quick start will show how to do the following:

* Install everything needed to use Bowtie.
* Write an app connecting a slider to a plot.
* How to deploy to Heroku.


Install Node
------------

Bowtie uses `npm <https://www.npmjs.com/>`_ and
`yarn <https://yarnpkg.com/>`_ to install the javascript libraries
and `webpack <https://webpack.github.io/>`_ to compile the application.
We need to install both of these.

MacOS Install
^^^^^^^^^^^^^

On MacOS, I recommend using `Homebrew <http://brew.sh/>`_ to get npm::

    brew install node

Then we can use npm to install webpack and yarn globally::

    npm install -g webpack yarn

Install Bowtie
--------------

To install the latest release::

    pip install bowtie

To install bleeding edge, if you are using Python 3 you can use `flit <http://flit.readthedocs.io/en/latest/index.html>`_,  to install::

    flit install

If you are on Python 2, create a wheel with flit in Python 3, then
install that wheel with Python 2::

    py3> flit wheel
    py2> pip install dist/bowtie*.whl

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
    freq_slider = Nouislider(caption='frequency', mininum=1, maximum=10, start=5)

Next we'll create a listener that generates a plot on slider changes::

    def listener(freq):
        freq = float(freq[0])
        t = np.linspace(0, 10, 100)
        sine_plot.do_all(pw.line(t, np.sin(freq * t)).to_json())

The :py:class:`bowtie.control.Nouislider` component sends its values as a list of strings so we had to cast it to a float.

Lastly we need to build the application by laying out the components and connecting listeners to events.
The ``Layout`` class handles this and we put this logic into a function.
Bowtie provides a decorator, ``command``, which we'll use to make a simple command line interface.
To finish, we simply wrap the function with the ``command`` decorator::

    from bowtie import command
    @command
    def construct(path)
        from bowtie import Layout
        layout = Layout(directory=path)
        layout.add_controller(freq_slider)
        layout.add_visual(sine_plot)
        layout.subscribe(freq_slider.on_change, listener)
        layout.build()

The ``path`` argument is optional, but it allows you to specify a directory through command line arguments.

Now take a look at the CLI we just created by running this script::

    python app.py

The output should look something like this::

    Usage: app.py [-p <path>] [--help] COMMAND [ARGS]...

      Bowtie CLI to help build and run your app.

    Options:
      -p, --path TEXT  Path to build the app.
      --help           Show this message and exit.

    Commands:
      build  Writes the app, downloads the packages, and...
      dev    Recompiles the app for development.
      prod   Recompiles the app for production.
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

* Create a Procfile, you can see `bowtie-demo <https://github.com/jwkvam/bowtie-demo/>`_ for an example.
* Create requirements files, again see `bowtie-demo <https://github.com/jwkvam/bowtie-demo/>`_ for an example.
* Rebuild with production settings with webpack, by default Bowtie uses development::

      cd build
      webpack -p

* Commit the following files to your repo::

      build/src/server.py
      build/src/templates
      build/src/static

* Finally push your repo to Heroku!
