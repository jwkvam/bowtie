import PropTypes from 'prop-types';
import React from 'react';
import { Checkbox } from 'antd';
import { storeState } from './utils';
const msgpack = require('msgpack-lite');

const CheckboxGroup = Checkbox.Group;


export default class Checkboxes extends React.Component {
    constructor(props) {
        super(props);
        var local = sessionStorage.getItem(this.props.uuid);
        if (local === null) {
            this.state = {value: this.props.default, options: this.props.options};
        } else {
            this.state = JSON.parse(local);
        }
    }

    handleChange = value => {
        console.log('checked values');
        console.log(value);
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
            <CheckboxGroup
                options={this.state.options}
                defaultValue={this.props.defaults}
                value={this.state.value}
                onChange={this.handleChange} 
            />
        );
    }
}

Checkboxes.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    options: PropTypes.array.isRequired,
    defaults: PropTypes.array.isRequired,
};
