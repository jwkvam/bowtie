import PropTypes from 'prop-types';
import React from 'react';
import { Slider } from 'antd';
import 'antd/dist/antd.css';

var msgpack = require('msgpack-lite');

export default class AntSlider extends React.Component {
    constructor(props) {
        super(props);
        var uuid = this.props.uuid;
        var socket = this.props.socket;
        this.state = {
            value: this.props.start,
            max: this.props.max,
            min: this.props.min
        };
        socket.on(uuid + '#get', this.getValue);
        socket.on(uuid + '#value', this.setValue);
        socket.on(uuid + '#inc', this.incValue);
        socket.on(uuid + '#min', this.setMax);
        socket.on(uuid + '#max', this.setMin);
        socket.on(uuid + '#min_max_value', this.setMinMaxValue);
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.value));
    }

    setValue = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({value: msgpack.decode(arr)});
    }

    setMax = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({max: msgpack.decode(arr)});
    }

    setMin = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({min: msgpack.decode(arr)});
    }

    setMinMaxValue = data => {
        var arr = new Uint8Array(data['data']);
        var value = msgpack.decode(arr);
        this.setState({min: value[0], max: value[1], value: value[2]});
    }

    incValue = data => {
        var arr = new Uint8Array(data['data']);
        var value = msgpack.decode(arr);
        this.setState({value: this.state.value + value});
    }

    onChange = value => {
        this.setState({value: value});
        this.props.socket.emit(this.props.uuid + '#change', msgpack.encode(value));
    }

    onAfterChange = value => {
        this.props.socket.emit(this.props.uuid + '#after_change', msgpack.encode(value));
    }

    render() {
        return (
            <Slider
                range={this.props.range}
                value={this.state.value}
                min={this.state.min}
                max={this.state.max}
                step={this.props.step}
                marks={this.props.marks}
                onChange={this.onChange}
                onAfterChange={this.onAfterChange}
            />
        );
    }
}

AntSlider.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    min: PropTypes.number.isRequired,
    max: PropTypes.number.isRequired,
    range: PropTypes.bool.isRequired,
    start: PropTypes.oneOfType([
        PropTypes.number,
        PropTypes.array
    ]).isRequired,
    step: PropTypes.number.isRequired,
    marks: PropTypes.object.isRequired,
};
