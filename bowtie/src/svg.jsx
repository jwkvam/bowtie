import PropTypes from 'prop-types';
import React from 'react';

var msgpack = require('msgpack-lite');

export default class SVG extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: null};
    }

    handleChange(value) {
        this.setState({value});
        this.props.socket.emit(this.props.uuid + '#change', msgpack.encode(value));
    }

    image = data => {
        var arr = new Uint8Array(data['data']);
        var str = msgpack.decode(arr);
        if (!this.props.preserveAspectRatio) {
            var idx = str.indexOf(' ');
            str = str.slice(0, idx) + ' preserveAspectRatio="none"' + str.slice(idx);
        }
        this.setState({value: str});
    }

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#image', this.image);
    }

    render () {
        return (
            <img
                width={'100%'}
                height={'100%'}
                src={'data:image/svg+xml;base64,' + btoa(this.state.value)}
            />
        );
    }
}

SVG.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    preserveAspectRatio: PropTypes.object.isRequired,
};
