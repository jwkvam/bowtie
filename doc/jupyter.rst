Jupyter Integration
===================

Bowtie can run a dashboard defined in a Jupyter notebook.
Create your app in the same fashion you would in a script.
Instead of using a ``main`` function decorated with ``@command``,
we use an IPython magic::

    app = App()
    server = %bowtie app

This will run the Bowtie app and create an iframe to view the dashboard.
The server object is the return value of a subprocess run.
When you wish to terminate the server call ``terminate`` on it::

    server.terminate()
