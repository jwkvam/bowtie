.. Bowtie documentation master file, created by
   sphinx-quickstart on Fri Aug 19 23:07:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Create New Components
=====================

Bowtie is designed to not make it terribly onerous to make new components.
That being said, we need to write a little bit of code in different places
so an enduser can use it.

#. Create new React class
#. Create visual or control class in Python
#. Create events that the React class supports

To walk through this process I'll use the dropdown component, since that
touches on many interesting pieces.

React Class
-----------

The dropdown component leverages a popular
`react dropdown component <http://jedwatson.github.io/react-select/>`_
to do the heavy lifting.
First we start by importing react and the component::

    import React from 'react';
    import Select from 'react-select';
    import 'react-select/dist/react-select.css';

We also imported the default styling so it looks reasonable.
We can do this because we're using `webpack <https://webpack.github.io>`_
to compile the application.

Next we will define the properties that the React class will hold.
This defines how the Python code can initialize the component.
We always need ``uuid`` and ``socket`` properties since they make
it possible for the Python backend to communicate with the React object.
This component has allows for multiple selection so that will be a ``bool``
property.
We'll also make an ``initOptions`` property which will let us set an
initial list of options to populate the dropdown.
Now that we have that defined let's write it in code::

    DropDown.propTypes = {
        uuid: React.PropTypes.string.isRequired,
        socket: React.PropTypes.object.isRequired,
        multi: React.PropTypes.bool.isRequired,
        initOptions: React.PropTypes.array
    };

Now we will create the class::

    export default class DropDown extends React.Component {
        ...
    }

Everything from now we'll write as functions in the class body.
First comes the constructor::

    constructor(props) {
        super(props);
        this.state = {value: null};
        this.state.options = this.props.initOptions;
        this.handleChange = this.handleChange.bind(this);
        this.getValue = this.getValue.bind(this);
    }



    handleChange(value) {
        this.setState({value});
        this.props.socket.emit(this.props.uuid + '#change', value);
    }

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getValue);
        socket.on(uuid + '#options', (data) => {
            this.setState({value: null, options: JSON.parse(data)});
        });
    }

    getValue(data, fn) {
        fn(this.state.value);
    }

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
