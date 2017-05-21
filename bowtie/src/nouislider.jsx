import PropTypes from 'prop-types';
import React from 'react';
import noUiSlider from 'nouislider/distribute/nouislider.min.js';
import 'nouislider/distribute/nouislider.css';

var msgpack = require('msgpack-lite');

export default class Nouislider extends React.Component {
    constructor(props) {
        super(props);
        this.createSlider = this.createSlider.bind(this);
        this.getValue = this.getValue.bind(this);
    }

    createSlider() {
        var slider = this.slider = noUiSlider.create(this.sliderContainer,
            {...this.props}
        );

        var uuid = this.props.uuid;
        var socket = this.props.socket;

        slider.on('update', function (data) {
            socket.emit(uuid + '#update', msgpack.encode(data));
        });
        slider.on('change', function (data) {
            socket.emit(uuid + '#change', msgpack.encode(data));
        });
        slider.on('slide', function (data) {
            socket.emit(uuid + '#slide', msgpack.encode(data));
        });
        slider.on('set', function (data) {
            socket.emit(uuid + '#set', msgpack.encode(data));
        });
        slider.on('start', function (data) {
            socket.emit(uuid + '#start', msgpack.encode(data));
        });
        slider.on('end', function (data) {
            socket.emit(uuid + '#end', msgpack.encode(data));
        });
    }

    componentDidMount() {
        if (this.props.disabled) this.sliderContainer.setAttribute('disabled', true);
        else this.sliderContainer.removeAttribute('disabled');

        this.createSlider();
        var uuid = this.props.uuid;
        var socket = this.props.socket;

        socket.on(uuid + '#get', this.getValue);
    }

    getValue(data, fn) {
        fn(msgpack.encode(this.slider.get()));
    }

    componentDidUpdate() {
        if (this.props.disabled) this.sliderContainer.setAttribute('disabled', true);
        else this.sliderContainer.removeAttribute('disabled');
        this.slider.destroy();
        this.createSlider();
    }

    componentWillUnmount() {
        this.slider.destroy();
    }

    render() {
        return (
            <div ref={(slider) => this.sliderContainer = slider} />
        );
    }
}

Nouislider.propTypes = {
    // http://refreshless.com/nouislider/slider-options/#section-animate
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    animate: PropTypes.bool,
    // http://refreshless.com/nouislider/behaviour-option/
    behaviour: PropTypes.string,
    // http://refreshless.com/nouislider/slider-options/#section-Connect
    connect: PropTypes.oneOfType([
        PropTypes.oneOf(['lower', 'upper']),
        PropTypes.bool
    ]),
    // http://refreshless.com/nouislider/slider-options/#section-cssPrefix
    cssPrefix: PropTypes.string,
    // http://refreshless.com/nouislider/slider-options/#section-orientation
    direction: PropTypes.oneOf(['ltr', 'rtl']),
    // http://refreshless.com/nouislider/more/#section-disable
    disabled: PropTypes.bool,
    // http://refreshless.com/nouislider/slider-options/#section-limit
    limit: PropTypes.number,
    // http://refreshless.com/nouislider/slider-options/#section-margin
    margin: PropTypes.number,
    // http://refreshless.com/nouislider/events-callbacks/#section-change
    // onChange: React.PropTypes.func,
    // http://refreshless.com/nouislider/events-callbacks/#section-update
    // onSlide: React.PropTypes.func,
    // http://refreshless.com/nouislider/events-callbacks/#section-slide
    // onUpdate: React.PropTypes.func,
    // http://refreshless.com/nouislider/slider-options/#section-orientation
    orientation: PropTypes.oneOf(['horizontal', 'vertical']),
    // http://refreshless.com/nouislider/pips/
    pips: PropTypes.object,
    // http://refreshless.com/nouislider/slider-values/#section-range
    range: PropTypes.object.isRequired,
    // http://refreshless.com/nouislider/slider-options/#section-start
    start: PropTypes.arrayOf(PropTypes.number).isRequired,
    // http://refreshless.com/nouislider/slider-options/#section-step
    step: PropTypes.number,
    // http://refreshless.com/nouislider/slider-options/#section-tooltips
    tooltips: PropTypes.oneOfType([
        PropTypes.bool,
        PropTypes.arrayOf(
            PropTypes.shape({
                to: PropTypes.func
            })
        )
    ])
};
