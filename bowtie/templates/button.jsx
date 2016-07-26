import React from 'react';
import Button from 'react-button';


export default class SimpleButton extends React.Component {

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(event) {
        console.log('clicked');
        this.props.socket.emit(this.props.uuid + '#click');
    }

    render() {
        // var hw = get_height_width();
        // var height = Math.floor(hw[1] / this.rops.rows);
        // var width = Math.floor((hw[0] * 9 / 10) / this.props.columns);
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
