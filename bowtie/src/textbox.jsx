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
        socket.on(uuid + '#text', this.setValue);
    }

    setValue = (data, fn) => {
        var arr = new Uint8Array(data['data']);
        this.setState({value: msgpack.decode(arr)});
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
                value={this.state.value}
                type={this.props.type}
                placeholder={this.props.placeholder}
                defaultValue={this.state.value}
                onPressEnter={this.onPressEnter}
                onChange={this.onChange}
                autosize={this.props.autosize}
                disabled={this.props.disabled}
                size={this.props.size}
            />
        );
    }
}

Textbox.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    type: React.PropTypes.string.isRequired,
    autosize: React.PropTypes.bool.isRequired,
    disabled: React.PropTypes.bool.isRequired,
    socket: React.PropTypes.object.isRequired,
    placeholder: React.PropTypes.string.isRequired,
    size: React.PropTypes.string.isRequired,
};
