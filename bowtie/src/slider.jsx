import React from 'react';
import { Slider } from 'antd';
import 'antd/dist/antd.css';

var msgpack = require('msgpack-lite');

export default class AntSlider extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: this.props.start};
        // this.createSlider = this.createSlider.bind(this);
        // this.getValue = this.getValue.bind(this);
    }

    // createSlider() {
    //     var slider = this.slider = nouislider.create(this.sliderContainer,
    //         {...this.props}
    //     );
    //
    //     var uuid = this.props.uuid;
    //     var socket = this.props.socket;
    //
    //     slider.on('update', function (data) {
    //         socket.emit(uuid + '#update', msgpack.encode(data));
    //     });
    //     slider.on('change', function (data) {
    //         socket.emit(uuid + '#change', msgpack.encode(data));
    //     });
    //     slider.on('slide', function (data) {
    //         socket.emit(uuid + '#slide', msgpack.encode(data));
    //     });
    //     slider.on('set', function (data) {
    //         socket.emit(uuid + '#set', msgpack.encode(data));
    //     });
    //     slider.on('start', function (data) {
    //         socket.emit(uuid + '#start', msgpack.encode(data));
    //     });
    //     slider.on('end', function (data) {
    //         socket.emit(uuid + '#end', msgpack.encode(data));
    //     });
    // }

    componentDidMount() {
        var uuid = this.props.uuid;
        var socket = this.props.socket;
        socket.on(uuid + '#get', this.getValue);
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.value));
    }

    // componentDidUpdate() {
    //     if (this.props.disabled) this.sliderContainer.setAttribute('disabled', true);
    //     else this.sliderContainer.removeAttribute('disabled');
    //     this.slider.destroy();
    //     this.createSlider();
    // }

    // componentWillUnmount() {
    //     this.slider.destroy();
    // }

    onChange = value => {
        this.setState({value: value});
        this.props.socket.emit(this.props.uuid + '#change', msgpack.encode(value));
    }

    onAfterChange = value => {
        this.props.socket.emit(this.props.uuid + '#after_change', msgpack.encode(value));
    }

    render() {
        return (
            <Slider
                range={this.props.range}
                value={this.state.value}
                min={this.props.min}
                max={this.props.max}
                step={this.props.step}
                marks={this.props.marks}
                onChange={this.onChange}
                onAfterChange={this.onAfterChange}
            />
        );
    }
}

AntSlider.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    min: React.PropTypes.number.isRequired,
    max: React.PropTypes.number.isRequired,
    range: React.PropTypes.bool.isRequired,
    start: React.PropTypes.oneOfType([
        React.PropTypes.number,
        React.PropTypes.array
    ]).isRequired,
    step: React.PropTypes.number.isRequired,
    marks: React.PropTypes.object.isRequired,
};
