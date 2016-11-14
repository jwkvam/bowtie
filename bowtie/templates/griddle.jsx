import React from 'react';
import Griddle from 'griddle-react';

var msgpack = require('msgpack-lite');

function get_height_width() {
    var w = window,
        d = document,
        e = d.documentElement,
        g = d.getElementsByTagName('body')[0],
        x = w.innerWidth || e.clientWidth || g.clientWidth,
        y = w.innerHeight|| e.clientHeight|| g.clientHeight;
    return [x, y];
}

export default class SmartGrid extends React.Component {

    constructor(props) {
        super(props);
        this.state = {};
        this.state.data = [];
        this.getData = this.getData.bind(this);
    }

    getData(data, fn) {
        fn(msgpack.encode(this.state.data));
    }

    componentDidMount() {
        var socket = this.props.socket;

        socket.on(this.props.uuid + '#update', (data) => {
            var arr = new Uint8Array(data['data']);
            this.setState({data: msgpack.decode(data)});
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
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    columns: React.PropTypes.array.isRequired,
    resultsPerPage: React.PropTypes.number.isRequired
};
