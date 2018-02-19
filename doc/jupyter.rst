Jupyter Integration
===================

Bowtie can run a dashboard defined in a Jupyter notebook.
Create your app in the same fashion you would in a script.
Instead of using a ``main`` function decorated with ``@command``,
we use an IPython magic::

    app = App()
    %bowtie app

This will run the Bowtie app and create an iframe to view the dashboard.
When you want to stop the Bowtie app use the following magic::

    %bowtie_stop
