import PropTypes from 'prop-types';
import React from 'react';
import { Switch, LocaleProvider } from 'antd';
import enUS from 'antd/lib/locale-provider/en_US';
import { storeState } from './utils';

var msgpack = require('msgpack-lite');

export default class Toggle extends React.Component {
    constructor(props) {
        super(props);
        var local = sessionStorage.getItem(this.props.uuid);
        if (local === null) {
            this.state = { checked: this.props.defaultChecked };
        } else {
            this.state = JSON.parse(local);
        }
    }

    handleChange = checked => {
        this.setState({ checked: checked });
        storeState(this.props.uuid, this.state, { checked: checked });
        this.props.socket.emit(this.props.uuid + '#switch', msgpack.encode(checked));
    };

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getValue);
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.checked));
    };

    render() {
        return (
            <LocaleProvider locale={enUS}>
                <Switch
                    checked={this.state.checked}
                    defaultChecked={this.props.defaultChecked}
                    onChange={this.handleChange}
                />
            </LocaleProvider>
        );
    }
}

Toggle.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    defaultChecked: PropTypes.bool.isRequired,
};
