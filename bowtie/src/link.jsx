import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import React from 'react';

// export default Link;

export default class ALink extends React.Component {

    render() {
        return (
            <Link to={this.props.to}>ALINK</Link>
        );
    }
}

ALink.propTypes = {
    to: PropTypes.string,
    uuid: PropTypes.string,
    socket: PropTypes.object
};

// export default class Link extends React.Component {
//     constructor(props) {
//         super(props);
//         this.updateLocation = this.updateLocation.bind(this);
//     }
//
//     updateLocation() {
//         // const {href, refresh} = this.props;
//         var refresh = false;
//         if (refresh) {kk
//             window.location.pathname = this.props.href;
//         } else {
//             window.history.pushState({}, '', this.props.href);
//             window.dispatchEvent(new Event('onpushstate'));
//         }
//     }
//
//     render() {
//         // const {className, style, id} = this.props;
//         #<{(|
//          * ideally, we would use cloneElement however
//          * that doesn't work with dash's recursive
//          * renderTree implementation for some reason
//          |)}>#
//         return (
//             <a onClick={this.updateLocation}>
//                 A link
//             </a>
//         );
//     }
// }
// //  {this.props.children}
//                // className={className}
//                // style={style}
//
// Link.propTypes = {
//     href: PropTypes.string,
//     uuid: PropTypes.string.isRequired,
//     socket: PropTypes.object.isRequired
//     // refresh: PropTypes.bool,
//     // className: PropTypes.string,
//     // style: PropTypes.object,
//     // id: PropTypes.string,
//     // children: PropTypes.node
// };
// //
// // Link.defaultProps = {
// //     refresh: false
// // };
