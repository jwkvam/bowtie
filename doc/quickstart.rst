.. Bowtie documentation master file, created by
   sphinx-quickstart on Fri Aug 19 23:07:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Quick Start
===========

This quick start will show how to do the following.

* Install everything needed to use Bowtie.
* Write an app connecting a slider to a plot.
* How to deploy to Heroku.


Install Node
------------

Bowtie uses `npm <https://www.npmjs.com/>`_ to install the javascript libraries
and `webpack <https://webpack.github.io/>`_ to compile the application.
We need to install both of these.

MacOS Install
^^^^^^^^^^^

On MacOS, I recommend using `Homebrew <http://brew.sh/>`_ to get npm::

    brew install node

Then we can use npm to install webpack globally::

    npm install -g webpack

Install Bowtie
--------------

To install the latest version::

    pip install bowtie

To install bleeding edge you can create a wheel with
`flit <http://flit.readthedocs.io/en/latest/index.html>`_, then install it with pip::

    flit wheel
    pip install dist/bowtie*.whl

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

Next we'll create a listener to listener that generates a plot on slider changes::

    def listener(freq):
        t = np.linspace(0, 10, 100)
        sine_plot.do_all(pw.line(t, np.sin(freq * t)).to_json())

Lastly we need to build the application by layout the components and connecting listeners to events.
We do this in the main block::
    
    if __name__ == "__main__":
        from bowtie import Layout
        layout = Layout()
        layout.add_controller(freq_slider)
        layout.add_visual(sine_plot)
        layout.subscribe(freq_slider.on_change, listener)
        layout.build(debug=False)

Now we just need to execute the python script we wrote::

    python app.py

This will construct the app, install the javascript libraries and compile your project.
Once it's done you should be able to run the following to launch your app::

    ./build/src/server.py

That will launch the app locally and you should be able to access it at http://localhost:9991.

Deploy to Heroku
----------------

This isn't streamlined right now but you can try the following approach.
For example, this was done to create `bowtie-demo <https://github.com/jwkvam/bowtie-demo/>`_ so you may refer to that.

* Create a Procfile, you can see bowtie-demo for an example.
* Create requirements files, again see bowtie-demo for an example.
* Rebuild with production settings with webpack, by default Bowtie uses development::
      
      cd build
      webpack -p

* Commit the following files to your repo::
      
      build/src/server.py
      build/src/templates
      build/src/static

* Finally push your repo to Heroku!
