import React from 'react';
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

    componentDidMount() {
        this.props.socket.on(this.props.uuid + '#update', (data) => {
            this.setState({data: JSON.parse(data)});
        });
    }

    render() {
        return (
            <Griddle
                results={this.state.data}
                showFilter={true}
                showSettings={true}
                />
        );
    }
}

SmartGrid.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired
};
