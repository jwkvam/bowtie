.. Bowtie documentation master file, created by
   sphinx-quickstart on Fri Aug 19 23:07:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Architecture
============

Read this section if you are interested in hacking on Bowtie or understanding how it works. Essentially, Bowtie works by using SocketIO to communicate between React and Python.

.. graphviz::

    digraph foo {
        "Bowtie App" -> {"Browser 1";"Browser 2"} [dir="both",label="socket.io"];
        bgcolor="transparent";
    }

React
-----
All the available components are associated with a React class.
At a minimum each class must have a ``uuid`` and ``socket`` prop.
The ``uuid`` prop is a unique identifier which is used to name the message being sent.
The ``socket`` prop is a socketio connection.

Flask
-----
Bowtie attempts to abstract away the Flask interface.
Admittedly Flask is not difficult to learn but ultimately I wanted a library
which required little boilerplate.

If you want to tinker with the Flask app, you can edit the ``server.py`` file that
gets generated during the build phase.

SocketIO
--------
SocketIO binds the Python backend code to the React frontend.
Python uses the `Flask-SocketIO <https://flask-socketio.readthedocs.io/en/latest/>`_
extension and the frontend uses `socket.io-client <https://www.npmjs.com/package/socket.io-client>`_.

Events
------
Almost every component has events associated with it.
For example, a slider generates events when the user moves the slider.
In Bowtie, these events are class attributes with the prefix ``on_``.
With the App class you can subscribe callbacks to events, so when an
event happens the callback is called with an argument that is related to the event.

Commands
--------
Many components have commands to update their state.
For example you can update the drop down list or update a plot.
The commands are instance functions that are prefixed ``do_``.
For example, to update a Plotly chart in Bowtie you can call ``do_all(dict)``,
and Plotly will update it's chart with the data and layout options defined in the dictionary.

Bowtie Application
------------------
There are a few key parts to any Bowtie application.

1. Define the app, components, and global state::

    app = App(rows=1, columns=1, sidebar=True)
    plotly = Plotly()
    dropdown = Dropdown(*config)
    global_dataset = SQLQuery(cool_data)

2. Layout the app, you can also do this globally,
   but this can keep the code better organized::

    def layout():
        app.add_sidebar(dropdown)
        app.add(plotly)
    app.layout = layout

2. Create what should happen in response to events::

    @app.subscribe(dropdown.on_change)
    def callback(dropdown_item):
        # compute something cool and plot it
        data = cool_stuff(global_dataset, dropdown_item)
        plotly.do_all(data)

3. Create a main function that simply returns the app.
   Then Bowtie knows how to build and serve the app::

    from bowtie import command
    @command
    def main():
        return app
