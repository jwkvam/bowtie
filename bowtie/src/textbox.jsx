import React from 'react';
import { Input } from 'antd';
import 'antd/dist/antd.css';

var msgpack = require('msgpack-lite');

export default class Textbox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: null};
    }

    componentDidMount() {
        var uuid = this.props.uuid;
        var socket = this.props.socket;
        socket.on(uuid + '#get', this.getValue);
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.value));
    }

    onPressEnter = value => {
        this.setState({value: value.target.value});
        this.props.socket.emit(this.props.uuid + '#enter', msgpack.encode(value.target.value));
    }

    onChange = value => {
        this.setState({value: value.target.value});
        this.props.socket.emit(this.props.uuid + '#change', msgpack.encode(value.target.value));
    }

    render() {
        return (
            <Input
                type={'text'}
                placeholder={this.props.placeholder}
                defaultValue={this.state.value}
                onPressEnter={this.onPressEnter}
                onChange={this.onChange}
                autosize={false}
                size={this.props.size}
            />
        );
    }
}

Textbox.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    placeholder: React.PropTypes.string.isRequired,
    size: React.PropTypes.string.isRequired,
};
