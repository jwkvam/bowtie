import React from 'react';
import Button from 'react-button';


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
            <Button 
                label={this.props.label} 
                onClick={this.handleClick}
                />
        );
    }
}

SimpleButton.propTypes = {
    label: React.PropTypes.string.isRequired,
    uuid: React.PropTypes.string.isRequired,
    socket: React.PropTypes.object.isRequired
};
