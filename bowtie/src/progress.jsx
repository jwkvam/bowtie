import React from 'react';
import {Circle} from 'rc-progress';
import 'rc-progress/assets/index.css';

var msgpack = require('msgpack-lite');

export default class Progress extends React.Component {
    constructor(props) {
        super(props);
        this.state = {percent: 0, visible: false};
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

    componentDidMount() {
        var uuid = this.props.uuid;
        var socket = this.props.socket;

        socket.on(uuid + '#percent', this.percent);
        socket.on(uuid + '#visible', this.visible);
        socket.on(uuid + '#inc', this.increment);
    }

    render() {
        if (this.state.visible) {
            return (
                <div style={{display: 'flex', flex: '1 1 0', alignItems: 'center', justifyContent: 'center', alignContent: 'center'}}>
                <Circle
                    percent={this.state.percent}
                    strokeWidth="6"
                    strokeLinecap="round"
                    strokeColor={this.props.color}
                    style={{width: '70%', height: '70%', alignSelf: 'center'}}
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

Progress.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    color: React.PropTypes.string.isRequired,
    children: React.PropTypes.any
};
