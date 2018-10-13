Authentication
==============

Bowtie provides simple basic authentication out of the box.
Better support for other authentication methods is planned for future releases.
Adding basic authentication to your app is designed to be easy and simple.
Simply create a ``BasicAuth`` instance and pass it the Bowtie app and a
dictionary with usernames as keys and passwords as values::

    from bowtie import App
    from bowtie.auth import BasicAuth
    app = App(__name__)
    basic_auth = BasicAuth(app, {
        'alice': 'secret1',
        'bob': 'secret2',
    })

To provide your own authentication you can implement the interface required by the
abstract ``Auth`` class.
This is not well supported or well documented at this time unfortunately.


.. autoclass:: bowtie.auth.Auth
    :members:

.. autoclass:: bowtie.auth.BasicAuth
    :members:
