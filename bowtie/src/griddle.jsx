import PropTypes from 'prop-types';
import React from 'react';
import Griddle from 'griddle-react';
import { storeState } from './utils';

var msgpack = require('msgpack-lite');

export default class SmartGrid extends React.Component {

    constructor(props) {
        super(props);
        this.getData = this.getData.bind(this);
        var local = sessionStorage.getItem(this.props.uuid);
        if (local === null) {
            this.state = {data: []};
        } else {
            this.state = JSON.parse(local);
        }
    }

    getData(data, fn) {
        fn(msgpack.encode(this.state.data));
    }

    componentDidMount() {
        var socket = this.props.socket;

        socket.on(this.props.uuid + '#update', (data) => {
            var arr = new Uint8Array(data['data']);
            arr = msgpack.decode(arr);
            this.setState({data: arr});
            storeState(this.props.uuid, this.state, {data: arr});
        });

        socket.on(this.props.uuid + '#get', this.getData);
    }

    render() {
        return (
            <Griddle
                data={this.state.data}
            />
        );
    }
}

SmartGrid.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired
};
