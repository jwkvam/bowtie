import React from 'react';

import 'fixed-data-table/dist/fixed-data-table.css';
import {Table, Column, Cell} from 'fixed-data-table';

function get_height_width() {
    var w = window,
        d = document,
        e = d.documentElement,
        g = d.getElementsByTagName('body')[0],
        x = w.innerWidth || e.clientWidth || g.clientWidth,
        y = w.innerHeight|| e.clientHeight|| g.clientHeight;
    return [x, y];
}

export default class FixedTable extends React.Component {

    constructor(props) {
        super(props);
        this.state = {columns: ['id', 'first', 'last'],
            data: [
                [1, 2, 3],
                ['John', 'Bob', 'Bob'],
                ['Bobson', 'Mclaren', 'Mclaren']
            ]};
    }

    render() {
        var hw = get_height_width();
        var height = Math.floor(hw[1] / this.props.rows);
        var width = Math.floor((hw[0] * 9 / 10) / this.props.columns);
        var headers = this.state.columns;
        var columns = this.state.data;
        return (
            <Table
                rowHeight={30}
                rowsCount={this.state.data.length}
                width={width}
                height={height}
                headerHeight={30}>
                {headers.map(function(name, i){
                    return (
                        <Column
                            header={<Cell>{name}</Cell>}
                            cell={<Cell data={columns[i]} />}
                            width={100}
                        />
                    );
                })}

            </Table>
        );
    }
}
                // <Column
                //   header={<Cell>Col 1</Cell>}
                //   cell={<Cell>Column 1 static content</Cell>}
                //   width={100}
                // />
                // <Column
                //   header={<Cell>Col 2</Cell>}
                //   cell={<Cell>Column 2 static content</Cell>}
                //   width={100}
                // />
                // <Column
                //   header={<Cell>Col 3</Cell>}
                //   cell={({rowIndex, ...props}) => (
                //     <Cell {...props}>
                //       Data for column 3: {this.state.data[rowIndex][2]}
                //     </Cell>
                //   )}
                //   width={100}
                // />

FixedTable.propTypes = {
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired,
    rows: React.PropTypes.number,
    columns: React.PropTypes.number
};
