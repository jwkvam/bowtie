import React from 'react';
import 'griddle-react/css/griddle.css';
import Griddle from 'griddle-react';

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
        this.state.data = [
            { id: '1', firstName: 'John', lastName: 'Bobson'},
            { id: '2', firstName: 'Bob', lastName: 'Mclaren'},
            { id: '3', firstName: 'Bob', lastName: 'Mclaren'},
        ];

    }

    render() {
        // var hw = get_height_width();
        // var height = Math.floor(hw[1] / this.props.rows);
        // var width = Math.floor((hw[0] * 9 / 10) / this.props.columns);
        return (
            <Griddle results={this.state.data} />
        );
    }
}

SmartGrid.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    rows: React.PropTypes.number,
    columns: React.PropTypes.number
};
