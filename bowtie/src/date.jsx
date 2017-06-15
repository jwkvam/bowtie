import PropTypes from 'prop-types';
import React from 'react';
import { DatePicker, LocaleProvider } from 'antd';
import enUS from 'antd/lib/locale-provider/en_US';
import 'antd/dist/antd.css';
// import 'antd/lib/date-picker/style/index.css';
const { MonthPicker, RangePicker } = DatePicker;

var msgpack = require('msgpack-lite');

export default class PickDates extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: null};
    }

    handleChange = (moment, ds) => {
        this.setState({value: moment});
        this.props.socket.emit(this.props.uuid + '#change', msgpack.encode(ds));
    }

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getValue);
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.value));
    }

    render () {
        if (this.props.date) {
            return (
                <LocaleProvider locale={enUS}>
                    <DatePicker
                        style={{ width: '100%' }}
                        value={this.state.value}
                        onChange={this.handleChange}
                        locale={enUS}
                    />
                </LocaleProvider>
            );
        } else if (this.props.month) {
            return (
                <LocaleProvider locale={enUS}>
                    <MonthPicker
                        style={{ width: '100%' }}
                        value={this.state.value}
                        onChange={this.handleChange}
                        locale={enUS}
                    />
                </LocaleProvider>
            );
        } else {
            return (
                <LocaleProvider locale={enUS}>
                    <RangePicker
                        style={{ width: '100%' }}
                        value={this.state.value}
                        onChange={this.handleChange}
                        locale={enUS}
                    />
                </LocaleProvider>
            );
        }
    }
}

PickDates.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    date: PropTypes.bool.isRequired,
    month: PropTypes.bool.isRequired,
    range: PropTypes.bool.isRequired,
};
