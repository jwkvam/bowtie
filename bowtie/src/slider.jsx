import React from 'react';
import { Slider } from 'antd';
import 'antd/dist/antd.css';

var msgpack = require('msgpack-lite');

export default class AntSlider extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: this.props.start};
    }

    componentDidMount() {
        var uuid = this.props.uuid;
        var socket = this.props.socket;
        socket.on(uuid + '#get', this.getValue);
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.value));
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
                min={this.props.min}
                max={this.props.max}
                step={this.props.step}
                marks={this.props.marks}
                onChange={this.onChange}
                onAfterChange={this.onAfterChange}
            />
        );
    }
}

AntSlider.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    min: React.PropTypes.number.isRequired,
    max: React.PropTypes.number.isRequired,
    range: React.PropTypes.bool.isRequired,
    start: React.PropTypes.oneOfType([
        React.PropTypes.number,
        React.PropTypes.array
    ]).isRequired,
    step: React.PropTypes.number.isRequired,
    marks: React.PropTypes.object.isRequired,
};
