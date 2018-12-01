import 'normalize.css';
import React from 'react';
import PropTypes from 'prop-types';

import { components } from './components';
import { str2ints } from './utils';

export class View extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            columns: this.props.columns,
            rows: this.props.rows,
            column_gap: this.props.column_gap,
            row_gap: this.props.row_gap,
            spans: this.props.spans,
            controllers: this.props.controllers,
            sidebar: this.props.sidebar,
        };
    }

    render() {
        var widgets = [];
        const controls = this.state.controllers.map(index => (
            <div key={index.toString()}>{components[index]}</div>
        ));
        for (const key in this.state.spans) {
            if (this.state.spans.hasOwnProperty(key)) {
                const comps = this.state.spans[key].map(number => (
                    <div key={number.toString}>{components[number]}</div>
                ));
                const rowcols = str2ints(key);
                widgets.push(
                    <div
                        key={key}
                        style={{
                            gridColumn: `${rowcols[1] + this.state.sidebar} / ${rowcols[3] +
                                this.state.sidebar}`,
                            gridRow: `${rowcols[0]} / ${rowcols[2]}`,
                            position: 'relative',
                        }}
                    >
                        {comps}
                    </div>,
                );
            }
        }

        return (
            <div
                style={{
                    display: 'grid',
                    gridTemplateColumns: this.state.columns,
                    gridTemplateRows: this.state.rows,
                    gridColumnGap: this.state.column_gap,
                    gridRowGap: this.state.row_gap,
                    margin: `${this.props.border}`,
                    width: '100%',
                    height: '100%',
                    minHeight: '100vh',
                    maxHeight: '100%',
                    minWidth: '100vw',
                    maxWidth: '100%',
                }}
            >
                {this.state.sidebar && (
                    <div
                        style={{
                            padding: `${this.props.border}`,
                            margin: `-${this.props.border}`,
                            marginRight: 0,
                            backgroundColor: `${this.props.background_color}`,
                            gridColumn: '1 / 2',
                            gridRow: '1 / -1',
                        }}
                    >
                        {controls}
                    </div>
                )}

                {widgets}
            </div>
        );
    }
}

View.propTypes = {
    uuid: PropTypes.string.isRequired,
    background_color: PropTypes.string.isRequired,
    spans: PropTypes.object.isRequired,
    controllers: PropTypes.arrayOf(PropTypes.number).isRequired,
    columns: PropTypes.string.isRequired,
    rows: PropTypes.string.isRequired,
    column_gap: PropTypes.string.isRequired,
    row_gap: PropTypes.string.isRequired,
    border: PropTypes.string.isRequired,
    sidebar: PropTypes.bool.isRequired,
};
