import React from 'react';
import Plotly from 'plotly.js';

export default class PlotlyPlot extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.props.initState;
    }

    // changeAll = (all) => {this.setState(all);}
    //

    shouldComponentUpdate(nextProps) {
        return true;
    }

    componentDidMount() {
        // let {data, layout, config} = this.props;
        Plotly.newPlot(this.container, this.state.data, this.state.layout); //, config);
        // if (this.props.onClick)
        var uuid = this.props.uuid;
        var socket = this.props.socket;
        // if (this.props.onClick)
        this.container.on('plotly_click', function (data) {

            var p0 = data.points[0];
            var datum = {
                n: p0.pointNumber,
                x: p0.x,
                y: p0.y,
            };
            console.log('clicked');
            console.log('data');
            socket.emit(uuid + '#click', datum);
        });
        // if (this.props.onBeforeHover)
        // this.container.on('plotly_beforehover', function (data) {
        //     socket.emit(uuid + '#beforehover', data);
        // });
        // // if (this.props.onHover)
        // this.container.on('plotly_hover', function (data) {
        //     socket.emit(uuid + '#hover', data);
        // });
        // // if (this.props.onUnHover)
        // this.container.on('plotly_unhover', function (data) {
        //     socket.emit(uuid + '#unhover', data);
        // });
        // // if (this.props.onSelected)
        // this.container.on('plotly_selected', function (data) {
        //     socket.emit(uuid + '#selected', data);
        // });

        socket.on(this.props.uuid + '#all', (data) => {
            this.setState(JSON.parse(data));
        });
        // socket.on(this.props.uuid + '#' + 'get', (data) => {
        //     console.log('get command!!!');
        //     console.log(data);
        //     console.log(uuid + '#put');
        //     socket.emit(uuid + '#put', [3]); //this.state);
        //     console.log('done seding');
        // });
        socket.on(this.props.uuid + '#' + 'get', function (data, fn) {
            console.log('get command!!!');
            console.log(data);
            console.log(uuid + '#put');
            // socket.emit(uuid + '#put'); //this.state);
            fn({hello: 'new data'});
            console.log('done seding');
        });
        // socket.emit(this.props.uuid + '#put', [3]);
    }

    // updateState(state) {
    //     console.log('updating...');
    //     this.state = state;
    // }

    // updateState = (ev) => this.setState({ text: ev.target.value });
    

    componentDidUpdate() {
        //TODO use minimal update for given changes
        this.container.data = this.state.data;
        this.container.layout = this.state.layout;
        // console.log(this.state);
        Plotly.redraw(this.container); //, this.state.data, this.state.layout);
    }

    componentWillUnmount() {
        this.container.removeAllListeners('plotly_click');
        this.container.removeAllListeners('plotly_beforehover');
        this.container.removeAllListeners('plotly_hover');
        this.container.removeAllListeners('plotly_unhover');
        this.container.removeAllListeners('plotly_selected');
    }

    render() {
        return (
            <div ref={(node) => this.container=node} />
        );
    }

}

PlotlyPlot.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    initState: React.PropTypes.object
};

    // onClick: React.PropTypes.func,
    // onBeforeHover: React.PropTypes.func,
    // onHover: React.PropTypes.func,
    // onUnHover: React.PropTypes.func,
    // onSelected: React.PropTypes.func
