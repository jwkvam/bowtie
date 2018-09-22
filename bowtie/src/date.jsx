import PropTypes from 'prop-types';
import React from 'react';
import { DatePicker, LocaleProvider } from 'antd';
import enUS from 'antd/lib/locale-provider/en_US';
const { MonthPicker, RangePicker } = DatePicker;
import { storeState } from './utils';
import moment from 'moment';

var msgpack = require('msgpack-lite');

export default class PickDates extends React.Component {
    constructor(props) {
        super(props);
        var local = sessionStorage.getItem(this.props.uuid);
        if (local === null) {
            this.state = {value: null, datestring: null};
        } else {
            local = JSON.parse(local);
            if (Array.isArray(local.value)) {
                local.value = local.value.map(x => moment(x));
            } else {
                local.value = moment(local.value);
            }
            this.state = local;
        }
    }

    handleChange = (mom, ds) => {
        this.setState({value: mom, datestring: ds});
        storeState(this.props.uuid, this.state, {value: mom, datestring: ds});
        this.props.socket.emit(this.props.uuid + '#change', msgpack.encode(ds));
    }

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getValue);
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.datestring));
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
