import PropTypes from 'prop-types';
import React from 'react';
import Select from 'react-select';
// Be sure to include styles at some point, probably during your bootstrapping
import 'react-select/dist/react-select.css';
import { storeState } from './utils';

var msgpack = require('msgpack-lite');

export default class Dropdown extends React.Component {
    constructor(props) {
        super(props);
        var local = sessionStorage.getItem(this.props.uuid);
        if (local === null) {
            this.state = {value: this.props.default, options: this.props.initOptions};
        } else {
            this.state = JSON.parse(local);
        }
    }

    handleChange = value => {
        this.setState({value: value});
        this.props.socket.emit(this.props.uuid + '#change', msgpack.encode(value));
        storeState(this.props.uuid, this.state, {value: value});
    }

    choose = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({value: arr});
        storeState(this.props.uuid, this.state, {value: arr});
    }

    newOptions = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({value: null, options: msgpack.decode(arr)});
        storeState(this.props.uuid, this.state, {value: null, options: msgpack.decode(arr)});
    }

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getValue);
        socket.on(uuid + '#options', this.newOptions);
        socket.on(uuid + '#choose', this.choose);
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.value));
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
}

Dropdown.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    multi: PropTypes.bool.isRequired,
    default: PropTypes.any,
    initOptions: PropTypes.array
};
