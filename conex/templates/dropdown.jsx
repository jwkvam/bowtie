import React from 'react';
import Select from 'react-select';
// Be sure to include styles at some point, probably during your bootstrapping
import 'react-select/dist/react-select.css';




export default class DropDown extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: this.props.options[0]};
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
    }

    getValue(data, fn) {
        fn(this.state.value);
    }

    render () {
        return (
            <Select
                name={this.props.name}
                value={this.state.value}
                options={this.props.options}
                onChange={this.handleChange}
            />
        );
    }
}

DropDown.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    name: React.PropTypes.string,
    options: React.PropTypes.array.isRequired
};
