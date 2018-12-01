import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import React from 'react';

export default class ALink extends React.Component {
    render() {
        return <Link to={this.props.to}>ALINK</Link>;
    }
}

ALink.propTypes = {
    to: PropTypes.string,
    uuid: PropTypes.string,
    socket: PropTypes.object,
};
