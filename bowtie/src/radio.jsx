import PropTypes from 'prop-types';
import React from 'react';
import { Radio } from 'antd';
import { storeState } from './utils';
const msgpack = require('msgpack-lite');

const RadioGroup = Radio.Group;

export default class Radios extends React.Component {
    constructor(props) {
        super(props);
        var local = sessionStorage.getItem(this.props.uuid);
        if (local === null) {
            this.state = { value: this.props.default, options: this.props.options };
        } else {
            this.state = JSON.parse(local);
        }
    }

    handleChange = value => {
        this.setState({ value: value });
        this.props.socket.emit(this.props.uuid + '#change', msgpack.encode(value));
        storeState(this.props.uuid, this.state, { value: value });
    };

    select = data => {
        var arr = msgpack.decode(new Uint8Array(data['data']));
        this.handleChange(arr);
    };

    newOptions = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({ value: null, options: msgpack.decode(arr) });
        storeState(this.props.uuid, this.state, { value: null, options: msgpack.decode(arr) });
    };

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getValue);
        socket.on(uuid + '#options', this.newOptions);
        socket.on(uuid + '#select', this.choose);
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.value));
    };

    render() {
        return (
            <RadioGroup
                options={this.state.options}
                value={this.state.value}
                onChange={this.handleChange}
            />
        );
    }
}

Radios.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    default: PropTypes.any,
    options: PropTypes.array,
};
