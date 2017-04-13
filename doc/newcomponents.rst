Create New Components
=====================

Bowtie is designed to not make it terribly onerous to make new components.
We need to write two new classes.

#. Create new React class
#. Create visual or control class in Python

To walk through this process I'll use the dropdown component, since that
touches on many interesting pieces.

React Class
-----------

The dropdown component leverages a popular
`react dropdown component <http://jedwatson.github.io/react-select/>`_
to do the heavy lifting.
First we start by importing react, msgpack and the component::

    import React from 'react';
    import Select from 'react-select';
    import 'react-select/dist/react-select.css';
    var msgpack = require('msgpack-lite');


We also imported the default styling so it looks reasonable.
We can do this because we're using `webpack <https://webpack.js.org/>`_
to compile the application.

Next we will define the properties that the React class will hold.
This defines how the Python code can initialize the component.
We always need ``uuid`` and ``socket`` properties since they make
it possible for the Python backend to communicate with the React object.
This component supports multiple selection and that will be a ``bool`` property.
We'll also make an ``initOptions`` property which will let us set an
initial list of options to populate the dropdown.
Now that we have that defined let's write it in code::

    Dropdown.propTypes = {
        uuid: React.PropTypes.string.isRequired,
        socket: React.PropTypes.object.isRequired,
        multi: React.PropTypes.bool.isRequired,
        initOptions: React.PropTypes.array
    };

Now we will create the class::

    export default class Dropdown extends React.Component {
        ...
    }

Everything from now we'll write as functions in the class body.
First we'll look at the render function::

    render () {
        return (
            <Select
                multi={this.props.multi}
                value={this.state.value}
                options={this.state.options}
                onChange={this.handleChange}
            />
        );
    }

This instantiates the component and allows us to set configuration options for the underlying component.
Note that ``this.state`` is mutable and ``this.prop`` is fixed.
For example, multiple selection cannot be changed but the drop down options can be changed.

Now we'll tell it how to communicate.
We do this after the component is created in the ``componentDidMount`` function::

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getValue);
        socket.on(uuid + '#options', (data) => {
            var arr = new Uint8Array(data['data']);
            this.setState({value: null, options: msgpack.decode(arr)});
        });
    }

Note that we have defined a command to be used through Python with ``do_options`` and
a ``get`` function so Python can get it's current state.
Next we define the constructor which initializes the state and binds ``this`` to those handlers::

    constructor(props) {
        super(props);
        this.state = {value: null};
        this.state.options = this.props.initOptions;
        this.handleChange = this.handleChange.bind(this);
        this.getValue = this.getValue.bind(this);
    }

Lastly we define the handlers referenced above::

    handleChange(value) {
        this.setState({value});
        this.props.socket.emit(this.props.uuid + '#change', value);
    }

    getValue(data, fn) {
        fn(this.state.value);
    }

Python Class
------------

Now that we have the React component defined, let's write the Python half.
We don't need to write much here, it's a little glue code.

First we'll define the class::

    class Dropdown(_Controller):
        _TEMPLATE = 'dropdown.jsx'
        _COMPONENT = 'Dropdown'
        _PACKAGE = 'react-select'
        _TAG = ('<Dropdown initOptions={{{options}}} '
                'multi={{{multi}}}'
                'socket={{socket}} '
                'uuid={{{uuid}}} '
                '/>')

We have defined a few component specific constants:

- ``_TEMPLATE``: Name of the file where the React class is defined.
- ``_COMPONENT``: Name of the React class (used to import the class).
- ``_PACKAGE``: Name of the NPM package used by the component.
- ``_TAG``: String used to instantiate the component.

We write the constructor who's main responsibility is creating the string to instantiate
the component in Javascript.
In Bowtie, this gets assigned to the ``_instantiate`` field::

    def __init__(self, options, multi=False, caption=''):
        super(Dropdown, self).__init__()

        self._instantiate = self._TAG.format(
            options=json.dumps(options),
            multi='true' if multi else 'false',
            uuid="'{}'".format(self._uuid)
        )
        self.caption = caption

Lastly we have one *event* (named "change"),
one *command* (named "options"),
and one *getter* (named "get").
We can create those by defining functions with the appropriate name and arguments,
metaclasses handle the rest::

    def on_change(self):
        pass

For the commands, we have the ability to just pass the data through to the React component::

    def do_options(self, data):
        return data

We can also preprocess the data to present an easier interface for the programmer::

    def do_options(self, labels, values):
        return [dict(label=l, value=v) for l, v in zip(labels, values)]

The main caveat here is we must ensure the data is serializable by msgpack.

For the getter we can write::

    def get(self, data):
        return data

We can use this getter to do post processing,
but here I just return the data as given to me from the React component.

Metaclass Parsing
~~~~~~~~~~~~~~~~~

A note about how commands, events, and getters are transformed into messages.

Events
######

Anything function that begins with ``on_`` is an event.
The message that ends up getting sent is ``on_{name}`` is ``{uuid}#name``.

Commands
########

Anything function that begins with ``do_`` is a command.
The message that ends up getting sent is ``do_{name}`` is ``{uuid}#name``.

Getters
#######

Anything function that begins with ``get_`` or is ``get`` is a getter.
The message that ends up getting sent is ``get_{name}`` is ``{uuid}#get`` or ``{uuid}#get_{name}``.
