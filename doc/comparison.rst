Comparison with Other Tools
===========================

Bowtie is designed to have a simple API to create dashboard applications quickly.
That being said let's compare this against similar Python libraries.
This section could use some help especially if you are familiar with one of the libraries listed.

Dash
----

From Plotly is `Dash <https://github.com/plotly/dash>`_
Even though both Bowtie and Dash allow you to develop a dashboard we have very different designs.

Layout API
~~~~~~~~~~

Dash uses HTML.
In order to layout your dash app you need to know a little HTML.
This can be a pro or con depending on your comfort with HTML.

Bowtie uses its own Pythonic API.
You don't need to know any HTML.
On the other hand you need to read the API to understand how to use it.

Events
~~~~~~

In my opinion, the callback and event system is much easier to use and more powerful in Bowtie.
The API is Pythonic so you don't have to memorize special strings.
You can distinguish between events and state.
You can update multiple components in a single callback.
Bowtie tries very hard to be simple to use and powerful.

Style
~~~~~

One area that Bowtie lacks in is styling.
Dash has powerful styling techniques.
If you need custom styling in Bowtie, you'll need to edit the generated HTML by hand.

Building and Running
~~~~~~~~~~~~~~~~~~~~

Running a Bowtie app consists of two steps: first "building" and then "running" the app.
The build process figures out what Javascript libraries are needed, creates HTML and Javascript files,
and finally uses Webpack to assemble it all into one Javascript file, ``bundle.js``.
Once the Javascript bundle is built the Bowtie app can be run.

Dash uses minified Javascript files and it doesn't pack them.
Overall this likely results in a better user experience for Dash users since packing the Javascript doesn't
result in a much smaller file or much better Javascript performance.

Dynamic Layout
~~~~~~~~~~~~~~

Bowtie's layouts are currently defined at build time.
Dash can dynamically change the layout.
This is a feature that I would like to add into Bowtie.

Source Code
~~~~~~~~~~~

Bowtie is a monolithic repo.
All the Python, Javascript, and HTML is in a single repo.
Dash is modular and has multiple repos for its core functionality, React components, and HTML components.

I believe Bowtie is easier to understand and maintain because everything is self-contained.
Instead it's harder to use custom components with Bowtie since they need to be included in the library itself.
This is decoupled in Dash so custom components are easier to develop.

Other
~~~~~

This has touched on some of the major differences.
There are many more however that I'll try to address eventually.

Bokeh
-----

This is the oldest dashboard tool in Python I'm aware of.
I think it hasn't been adopted much because of poor visibility and documentation.
To be fair I haven't used it a lot and only discovered it after I created Bowtie.

Shiny
-----

Not a Python library but is the gold standard.

.. todo::
    should try using shiny so I know what it's like
