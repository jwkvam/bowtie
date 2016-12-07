import React from 'react';
import { Button } from 'antd';
import 'antd/dist/antd.css';

export default class SimpleButton extends React.Component {

    constructor(props) {
        super(props);
    }

    handleClick = event => {
        this.props.socket.emit(this.props.uuid + '#click');
    }

    render() {
        return (
            <Button
            type="primary"
            onClick={this.handleClick} >
            {this.props.label}
            </Button>
        );
    }
}

SimpleButton.propTypes = {
    label: React.PropTypes.string.isRequired,
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired
};
