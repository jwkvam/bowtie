import PropTypes from 'prop-types';
import React from 'react';
import Griddle from 'griddle-react';

var msgpack = require('msgpack-lite');

export default class SmartGrid extends React.Component {

    constructor(props) {
        super(props);
        this.state = {data: []};
        this.getData = this.getData.bind(this);
    }

    getData(data, fn) {
        fn(msgpack.encode(this.state.data));
    }

    componentDidMount() {
        var socket = this.props.socket;

        socket.on(this.props.uuid + '#update', (data) => {
            var arr = new Uint8Array(data['data']);
            this.setState({data: msgpack.decode(arr)});
        });

        socket.on(this.props.uuid + '#get', this.getData);
    }

    render() {
        return (
            <Griddle
                results={this.state.data}
                showFilter={true}
                showSettings={true}
                useGriddleStyles={true}
                columns={this.props.columns}
                resultsPerPage={this.props.resultsPerPage}
            />
        );
    }
}

SmartGrid.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    columns: PropTypes.array.isRequired,
    resultsPerPage: PropTypes.number.isRequired
};
