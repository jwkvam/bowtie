import PropTypes from 'prop-types';
import React from 'react';
import { storeState } from './utils';

var msgpack = require('msgpack-lite');

export default class Bowhead extends React.Component {
    constructor(props) {
        super(props);
        var local = sessionStorage.getItem(this.props.uuid);
        if (local === null) {
            this.state = {value: this.props.initial};
        } else {
            this.state = JSON.parse(local);
        }
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.value));
    }

    setText = data => {
        var arr = new Uint8Array(data['data']);
        arr = msgpack.decode(arr);
        this.setState({value: arr});
        storeState(this.props.uuid, this.state, {value: arr});
    }

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getText);
        socket.on(uuid + '#text', this.setText);
    }

    render () {
        switch (this.props.size) {
        case 1:
            return <h1 dangerouslySetInnerHTML={{__html: this.state.value}} />;
        case 2:
            return <h2 dangerouslySetInnerHTML={{__html: this.state.value}} />;
        case 3:
            return <h3 dangerouslySetInnerHTML={{__html: this.state.value}} />;
        case 4:
            return <h4 dangerouslySetInnerHTML={{__html: this.state.value}} />;
        case 5:
            return <h5 dangerouslySetInnerHTML={{__html: this.state.value}} />;
        case 6:
            return <h6 dangerouslySetInnerHTML={{__html: this.state.value}} />;
        }
    }
}

Bowhead.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    initial: PropTypes.string.isRequired,
    size: PropTypes.number.isRequired
};
