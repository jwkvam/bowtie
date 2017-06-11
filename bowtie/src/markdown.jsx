import PropTypes from 'prop-types';
import React from 'react';

var msgpack = require('msgpack-lite');

export default class Markdown extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: this.props.initial};
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.value));
    }

    setText = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({value: msgpack.decode(arr)});
    }

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getText);
        socket.on(uuid + '#text', this.setText);
    }

    render () {
        return <div dangerouslySetInnerHTML={{__html: this.state.value}} />;
    }
}

Markdown.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    initial: PropTypes.string.isRequired
};
