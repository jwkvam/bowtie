import React from 'react';
import Plotly from 'plotly.js';
import cloneDeep from 'lodash.clonedeep';

var msgpack = require('msgpack-lite');

export default class PlotlyPlot extends React.Component {

    constructor(props) {
        super(props);
        this.selection = null;
        this.state = this.props.initState;
        this.resize = this.resize.bind(this);
        this.props.socket.on(this.props.uuid + '#all', (data) => {
            var arr = new Uint8Array(data['data']);
            this.setState(msgpack.decode(arr));
        });
        this.props.socket.on(this.props.uuid + '#get', this.getSelection);
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
        var uuid = this.props.uuid;
        var socket = this.props.socket;

        this.container.on('plotly_click', function (data) {
            var p0 = data.points[0];
            var datum = {
                n: p0.pointNumber,
                x: p0.x,
                y: p0.y,
                hover: p0.data.text[p0.pointNumber]
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
        // this.state.layout['autosize'] = false;
        // this.state.layout['height'] = parseFloat(parent.height);
        // this.state.layout['width'] = parseFloat(parent.width);
        var layout = this.state.layout;
        layout['autosize'] = false;
        layout['height'] = parseFloat(parent.height);
        layout['width'] = parseFloat(parent.width);
        Plotly.newPlot(this.container, this.state.data, cloneDeep(layout),
            {autosizable: false, displaylogo: false, fillFrame: true}); //, config);
        
        this.addListeners();
        // this.setState({layout: layout});
    }

    componentDidUpdate() {
        //TODO use minimal update for given changes
        // this.container.data = this.state.data;
        // this.container.layout = this.state.layout;
        //this.container.config = {autosizable: true, fillFrame: true, displaylogo: false};
        var parent = window.getComputedStyle(this.container.parentElement);
        var layout = this.state.layout;
        layout['autosize'] = false;
        layout['height'] = parseFloat(parent.height);
        layout['width'] = parseFloat(parent.width);

        // this.setState({layout: layout});
        Plotly.newPlot(this.container, this.state.data, cloneDeep(this.state.layout),
            {autosizable: false, displaylogo: false, fillFrame: true}); //, config);
        this.addListeners();

        // window.addEventListener('resize', this.resize);
    }

    componentWillUnmount() {
        this.props.socket.off(this.props.uuid + '#all');
        this.props.socket.off(this.props.uuid + '#get');
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
