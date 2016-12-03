import React from 'react';
import 'nouislider/src/nouislider.css';
import nouislider from 'nouislider';

var msgpack = require('msgpack-lite');

export default class Nouislider extends React.Component {
    constructor(props) {
        super(props);
        this.createSlider = this.createSlider.bind(this);
        this.getValue = this.getValue.bind(this);
    }

    createSlider() {
        var slider = this.slider = nouislider.create(this.sliderContainer,
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
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    animate: React.PropTypes.bool,
    // http://refreshless.com/nouislider/behaviour-option/
    behaviour: React.PropTypes.string,
    // http://refreshless.com/nouislider/slider-options/#section-Connect
    connect: React.PropTypes.oneOfType([
        React.PropTypes.oneOf(['lower', 'upper']),
        React.PropTypes.bool
    ]),
    // http://refreshless.com/nouislider/slider-options/#section-cssPrefix
    cssPrefix: React.PropTypes.string,
    // http://refreshless.com/nouislider/slider-options/#section-orientation
    direction: React.PropTypes.oneOf(['ltr', 'rtl']),
    // http://refreshless.com/nouislider/more/#section-disable
    disabled: React.PropTypes.bool,
    // http://refreshless.com/nouislider/slider-options/#section-limit
    limit: React.PropTypes.number,
    // http://refreshless.com/nouislider/slider-options/#section-margin
    margin: React.PropTypes.number,
    // http://refreshless.com/nouislider/events-callbacks/#section-change
    // onChange: React.PropTypes.func,
    // http://refreshless.com/nouislider/events-callbacks/#section-update
    // onSlide: React.PropTypes.func,
    // http://refreshless.com/nouislider/events-callbacks/#section-slide
    // onUpdate: React.PropTypes.func,
    // http://refreshless.com/nouislider/slider-options/#section-orientation
    orientation: React.PropTypes.oneOf(['horizontal', 'vertical']),
    // http://refreshless.com/nouislider/pips/
    pips: React.PropTypes.object,
    // http://refreshless.com/nouislider/slider-values/#section-range
    range: React.PropTypes.object.isRequired,
    // http://refreshless.com/nouislider/slider-options/#section-start
    start: React.PropTypes.arrayOf(React.PropTypes.number).isRequired,
    // http://refreshless.com/nouislider/slider-options/#section-step
    step: React.PropTypes.number,
    // http://refreshless.com/nouislider/slider-options/#section-tooltips
    tooltips: React.PropTypes.oneOfType([
        React.PropTypes.bool,
        React.PropTypes.arrayOf(
            React.PropTypes.shape({
                to: React.PropTypes.func
            })
        )
    ])
};
