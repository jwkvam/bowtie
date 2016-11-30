import React from 'react';

export default class SimpleButton extends React.Component {

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(event) {
        this.props.socket.emit(this.props.uuid + '#click');
    }

    render() {
        return (
            <button
            className='simple-button'
            onClick={this.handleClick}
            >{this.props.label}
            </button>
        );
    }
}

SimpleButton.propTypes = {
    label: React.PropTypes.string.isRequired,
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired
};
