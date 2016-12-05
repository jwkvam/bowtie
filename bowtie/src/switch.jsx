import React from 'react';
import { Switch, LocaleProvider } from 'antd';
import enUS from 'antd/lib/locale-provider/en_US';
import 'antd/dist/antd.css';

var msgpack = require('msgpack-lite');

export default class Toggle extends React.Component {
    constructor(props) {
        super(props);
        this.state = {checked: this.props.defaultChecked};
    }

    handleChange = (checked) => {
        this.setState({checked: checked});
        this.props.socket.emit(this.props.uuid + '#switch', msgpack.encode(checked));
    }

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getValue);
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.checked));
    }

    render () {
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
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    defaultChecked: React.PropTypes.bool.isRequired,
};
