import 'react-datagrid/index.css';
import React from 'react';
import DataGrid from 'react-datagrid';

export default class Table extends React.Component {

    render() {
        var data = [
            { id: '1', firstName: 'John', lastName: 'Bobson'},
            { id: '2', firstName: 'Bob', lastName: 'Mclaren'}
        ];
        var columns = [
            { name: 'firstName'},
            { name: 'lastName'}
        ];

        return (
            <DataGrid
                dataSource={data}
                idProperty='id'
                columns={columns}
            />
        );
    }

}

Table.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired
};
