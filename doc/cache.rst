.. Bowtie documentation master file, created by
   sphinx-quickstart on Fri Aug 19 23:07:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Cache
=====

Bowtie provides a simple key value store where you can store data with the client.
Keep in mind that if you store a large amount of data it will get transferred to and from the client
which could result in a poor user experience.
That being said, it can be very useful to store results from expensive computations.

.. autofunction:: bowtie.cache.save

.. autofunction:: bowtie.cache.load
