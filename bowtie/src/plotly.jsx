import PropTypes from 'prop-types';
import React from 'react';
import Plotly from 'plotly.js/dist/plotly.js';
import cloneDeep from 'lodash.clonedeep';

var msgpack = require('msgpack-lite');

export default class PlotlyPlot extends React.Component {

    constructor(props) {
        super(props);
        this.selection = null;
        this.click = null;
        this.hover = null;
        this.state = this.props.initState;
        this.resize = this.resize.bind(this);
        this.props.socket.on(this.props.uuid + '#all', (data) => {
            var arr = new Uint8Array(data['data']);
            this.setState(msgpack.decode(arr));
        });
        this.props.socket.on(this.props.uuid + '#get', this.getSelection);
        this.props.socket.on(this.props.uuid + '#get_select', this.getSelection);
        this.props.socket.on(this.props.uuid + '#get_click', this.getClick);
        this.props.socket.on(this.props.uuid + '#get_hover', this.getHover);
    }

    setSelection = data => {
        this.selection = data;
        this.props.socket.emit(this.props.uuid + '#select', msgpack.encode(data));
    }
    
    getSelection = (data, fn) => {
        fn(msgpack.encode(this.selection));
    }

    processPoint = data => {
        var p0 = data.points[0];
        var text = p0.data.text;
        var datum = {
            curve: p0.curveNumber,
            point: p0.pointNumber,
            x: p0.x,
            y: p0.y,
            // TODO this indexing needs to be checked
            hover: (text == null) ? null : text[p0.pointNumber]
        };
        return datum;
    }

    setClick = data => {
        var datum = this.processPoint(data);
        this.click = datum;
        this.props.socket.emit(this.props.uuid + '#click', msgpack.encode(datum));
    }

    getClick = (data, fn) => {
        fn(msgpack.encode(this.click));
    }

    setHover = data => {
        var datum = this.processPoint(data);
        this.hover = datum;
        this.props.socket.emit(this.props.uuid + '#hover', msgpack.encode(datum));
    }

    getHover = (data, fn) => {
        fn(msgpack.encode(this.hover));
    }

    resize() {
        Plotly.Plots.resize(this.container);
    }

    addListeners() {
        // this.container.on('plotly_beforehover', function (data) {
        // this.container.on('plotly_unhover', function (data) {
        this.container.on('plotly_selected', this.setSelection);
        this.container.on('plotly_click', this.setClick);
        this.container.on('plotly_hover', this.setHover);
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
        this.props.socket.off(this.props.uuid + '#get_select');
        this.props.socket.off(this.props.uuid + '#get_click');
        this.props.socket.off(this.props.uuid + '#get_hover');
        Plotly.purge(this.container);
    }

    render() {
        return (
            <div ref={(node) => this.container=node} />
        );
    }

}

PlotlyPlot.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    initState: PropTypes.object,
    rows: PropTypes.number,
    columns: PropTypes.number
};
