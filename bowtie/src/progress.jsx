import React from 'react';
import { Progress } from 'antd';
import 'antd/dist/antd.css';

var msgpack = require('msgpack-lite');

export default class CProgress extends React.Component {
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

    render() {
        if (this.state.visible) {
            return (
                <div style={{display: 'flex', flex: '1 1 0', alignItems: 'center', justifyContent: 'center', alignContent: 'center'}}>
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

CProgress.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    children: React.PropTypes.any
};
