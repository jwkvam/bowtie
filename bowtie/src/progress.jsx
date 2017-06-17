import PropTypes from 'prop-types';
import React from 'react';
import { Progress } from 'antd';
import 'antd/dist/antd.css';

var msgpack = require('msgpack-lite');

export default class AntProgress extends React.Component {
    constructor(props) {
        super(props);
        this.state = {percent: 0, visible: false, status: 'active'};
    }

    percent = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({percent: msgpack.decode(arr)});
    }

    increment = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({percent: this.state.percent + msgpack.decode(arr)});
    }

    visible = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({visible: msgpack.decode(arr)});
    }

    active = data => {
        this.setState({status: 'active'});
    }

    success = data => {
        this.setState({status: 'success'});
    }

    error = data => {
        this.setState({status: 'exception'});
    }

    componentDidMount() {
        var uuid = this.props.uuid;
        var socket = this.props.socket;

        socket.on(uuid + '#percent', this.percent);
        socket.on(uuid + '#visible', this.visible);
        socket.on(uuid + '#inc', this.increment);
        socket.on(uuid + '#active', this.active);
        socket.on(uuid + '#success', this.success);
        socket.on(uuid + '#error', this.error);
    }

    // Centering this component
    // http://stackoverflow.com/a/42934918/744520
    render() {
        if (this.state.visible) {
            return (
                <div style={{position: 'absolute',
                    top: '50%', left: '50%',
                    transform: 'translate(-50%, -50%)'
                }}>
                    <Progress
                        type="circle"
                        showInfo
                        status={this.state.status}
                        percent={this.state.percent}
                        style={{alignSelf: 'center'}}
                    />
                </div>
            );
        } else {
            return (
                this.props.children
            );
        }
    }
}

AntProgress.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    children: PropTypes.any
};
