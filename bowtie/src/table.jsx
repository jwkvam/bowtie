import PropTypes from 'prop-types';
import React from 'react';
import { Table, LocaleProvider } from 'antd';
import enUS from 'antd/lib/locale-provider/en_US';
import { storeState } from './utils';

var msgpack = require('msgpack-lite');

export default class AntTable extends React.Component {
    constructor(props) {
        super(props);
        var local = sessionStorage.getItem(this.props.uuid);
        if (local === null) {
            this.state = {
                data: [],
                columns: this.props.columns,
            };
        } else {
            this.state = JSON.parse(local);
        }
    }

    componentDidMount() {
        var uuid = this.props.uuid;
        var socket = this.props.socket;
        socket.on(uuid + '#data', this.newData);
        socket.on(uuid + '#columns', this.newColumns);
    }

    newData = (data, fn) => {
        var arr = new Uint8Array(data['data']);
        var datacols = msgpack.decode(arr);
        this.setState({ data: datacols[0], columns: datacols[1] });
        storeState(this.props.uuid, this.state, { data: datacols[0], columns: datacols[1] });
    };

    newColumns = (data, fn) => {
        var arr = new Uint8Array(data['data']);
        var columns = msgpack.decode(arr);
        this.setState({ columns: columns });
        storeState(this.props.uuid, this.state, { columns: columns });
    };

    render() {
        return (
            <LocaleProvider locale={enUS}>
                <Table
                    dataSource={this.state.data}
                    columns={this.state.columns}
                    size="small"
                    bordered={true}
                    pagination={{ pageSize: this.props.resultsPerPage }}
                    style={{ width: '100%' }}
                    scroll={{ y: false }}
                />
            </LocaleProvider>
        );
    }
}

AntTable.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    columns: PropTypes.array.isRequired,
    resultsPerPage: PropTypes.number.isRequired,
};
