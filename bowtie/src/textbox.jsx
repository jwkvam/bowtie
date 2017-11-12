import React from 'react';
import PropTypes from 'prop-types';
import { Input } from 'antd';
import 'antd/dist/antd.css';
import { storeState } from './utils';

var msgpack = require('msgpack-lite');

export default class Textbox extends React.Component {
    constructor(props) {
        super(props);
        var local = sessionStorage.getItem(this.props.uuid);
        if (local === null) {
            this.state = {value: null};
        } else {
            this.state = JSON.parse(local);
        }
    }

    componentDidMount() {
        var uuid = this.props.uuid;
        var socket = this.props.socket;
        socket.on(uuid + '#get', this.getValue);
        socket.on(uuid + '#text', this.setValue);
    }

    setValue = (data, fn) => {
        var arr = new Uint8Array(data['data']);
        arr = msgpack.decode(arr);
        this.setState({value: arr});
        storeState(this.props.uuid, this.state, {value: arr});
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.value));
    }

    onPressEnter = value => {
        this.setState({value: value.target.value});
        storeState(this.props.uuid, this.state, {value: value.target.value});
        this.props.socket.emit(this.props.uuid + '#enter', msgpack.encode(value.target.value));
    }

    onChange = value => {
        this.setState({value: value.target.value});
        storeState(this.props.uuid, this.state, {value: value.target.value});
        this.props.socket.emit(this.props.uuid + '#change', msgpack.encode(value.target.value));
    }

    render() {
        if (this.props.type == 'area') {
            return (
                <Input.TextArea
                    value={this.state.value}
                    placeholder={this.props.placeholder}
                    defaultValue={this.state.value}
                    onPressEnter={this.onPressEnter}
                    onChange={this.onChange}
                    autosize={this.props.autosize}
                    disabled={this.props.disabled}
                    size={this.props.size}
                />
            );
        } else {
            return (
                <Input
                    value={this.state.value}
                    placeholder={this.props.placeholder}
                    defaultValue={this.state.value}
                    onPressEnter={this.onPressEnter}
                    onChange={this.onChange}
                    disabled={this.props.disabled}
                    size={this.props.size}
                />
            );
        }
    }
}

Textbox.propTypes = {
    uuid: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    autosize: PropTypes.bool.isRequired,
    disabled: PropTypes.bool.isRequired,
    socket: PropTypes.object.isRequired,
    placeholder: PropTypes.string.isRequired,
    size: PropTypes.string.isRequired,
};
