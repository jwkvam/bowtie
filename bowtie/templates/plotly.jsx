import React from 'react';
import Plotly from 'plotly.js';
import cloneDeep from 'lodash.clonedeep';

var msgpack = require('msgpack-lite');

export default class PlotlyPlot extends React.Component {
    selection = 'inital';

    constructor(props) {
        super(props);
        this.state = this.props.initState;
        this.resize = this.resize.bind(this);
    }

    shouldComponentUpdate(nextProps) {
        return true;
    }

    setSelection = data => {
        this.selection = data;
        this.props.socket.emit(this.props.uuid + '#select', msgpack.encode(data));
    }
    
    getSelection = (data, fn) => {
        fn(msgpack.encode(this.selection));
    }

    resize() {
        Plotly.Plots.resize(this.container);
    }

    addListeners() {
        this.container.on('plotly_click', function (data) {

            var p0 = data.points[0];
            var datum = {
                n: p0.pointNumber,
                x: p0.x,
                y: p0.y,
            };
            socket.emit(uuid + '#click', msgpack.encode(datum));
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
        // if (this.props.onSelected)
        this.container.on('plotly_selected', this.setSelection);
    }

    componentDidMount() {
        // let {data, layout, config} = this.props;

        var parent = window.getComputedStyle(this.container.parentElement);
        this.state.layout['autosize'] = false;
        this.state.layout['height'] = parseFloat(parent.height);
        this.state.layout['width'] = parseFloat(parent.width);
        Plotly.newPlot(this.container, this.state.data, cloneDeep(this.state.layout),
            {autosizable: false, displaylogo: false, fillFrame: true}); //, config);
        
        // if (this.props.onClick)
        var uuid = this.props.uuid;
        var socket = this.props.socket;
        // if (this.props.onClick)

        socket.on(this.props.uuid + '#all', (data) => {
            var arr = new Uint8Array(data['data']);
            this.setState(msgpack.decode(arr));
        });
        // socket.on(this.props.uuid + '#' + 'get', (data) => {
        //     console.log('get command!!!');
        //     console.log(data);
        //     console.log(uuid + '#put');
        //     socket.emit(uuid + '#put', [3]); //this.state);
        //     console.log('done seding');
        // });
        socket.on(this.props.uuid + '#get', this.getSelection);
        this.addListeners();
            // console.log('get command!!!');
            // console.log(data);
            // console.log(uuid + '#put');
            // socket.emit(uuid + '#put'); //this.state);
            // fn(this.state.selection);
            // console.log('done seding');
        // });
        // socket.emit(this.props.uuid + '#put', [3]);
    }

    // updateState(state) {
    //     console.log('updating...');
    //     this.state = state;
    // }

    // updateState = (ev) => this.setState({ text: ev.target.value });
    

    componentDidUpdate() {
        //TODO use minimal update for given changes
        // this.container.data = this.state.data;
        // this.container.layout = this.state.layout;

        
        //this.container.config = {autosizable: true, fillFrame: true, displaylogo: false};
        var parent = window.getComputedStyle(this.container.parentElement);
        this.state.layout['autosize'] = false;
        this.state.layout['height'] = parseFloat(parent.height);
        this.state.layout['width'] = parseFloat(parent.width);
        Plotly.newPlot(this.container, this.state.data, cloneDeep(this.state.layout),
            {autosizable: false, displaylogo: false, fillFrame: true}); //, config);
        this.addListeners();

        // window.addEventListener('resize', this.resize);
    }

    componentWillUnmount() {
        Plotly.purge(this.container);
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
    initState: React.PropTypes.object,
    rows: React.PropTypes.number,
    columns: React.PropTypes.number
};
