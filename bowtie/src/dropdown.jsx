import PropTypes from 'prop-types';
import React from 'react';
import Select from 'react-select';
// Be sure to include styles at some point, probably during your bootstrapping
import 'react-select/dist/react-select.css';
import {observable} from "mobx";
import {observer} from "mobx-react";

var msgpack = require('msgpack-lite');

@observer
export default class Dropdown extends React.Component {

    @observable value = this.props.default; /* MobX managed instance state */
    @observable options = this.props.initOptions; /* MobX managed instance state */

    constructor(props, context) {
        super(props, context)
        // this.value = this.props.default;
        // this.options = this.props.initOptions;
    }
    // constructor(props) {
    //     super(props);
    //     // this.state = {value: this.props.default, options: this.props.initOptions};
    // }

    handleChange = value => {
        // this.setState({value});
        this.value = value;
        this.props.socket.emit(this.props.uuid + '#change', msgpack.encode(value));
    }

    choose = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({value: arr});
    }

    newOptions = data => {
        var arr = new Uint8Array(data['data']);
        // this.props.setOptions({ value: null, options: msgpack.decode(arr)});
        this.value = null;
        this.options = msgpack.decode(arr);
        // this.setState({value: null, options: msgpack.decode(arr)});
    }

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getValue);
        socket.on(uuid + '#options', this.newOptions);
        socket.on(uuid + '#choose', this.choose);
    }

    getValue = (data, fn) => {
        // fn(msgpack.encode(this.props.value));
        fn(msgpack.encode(this.value));
    }

    render () {
        return (
            <Select
                multi={this.props.multi}
                value={this.value}
                options={this.options.slice()}
                onChange={this.props.handleChange}
            />
        );
    }
}

Dropdown.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    multi: PropTypes.bool.isRequired,
    default: PropTypes.any,
    initOptions: PropTypes.array
};

//
// export const setOptions = (uuid, options) => {
//     return {
//         type: `${uuid}/options`,
//         options
//     };
// }
//
// // AppContainer.js
// const mapStateToProps = (state, ownProps) => ({  
//     value: state.value,
//     options: state.options,
// });
//
// const mapDispatchToProps = {  
//     setOptions,
// };
//
// export const reducer = (uuid) => (state, action) => {
//     switch(action.type) {
//         case `${uuid}/set_options`:
//             return Object.assign({}, state, {
//                 options: action.options
//             })
//         default:
//             return state
//     }
// }
