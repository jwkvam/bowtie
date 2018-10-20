import PropTypes from 'prop-types';
import React from 'react';
import { Checkbox } from 'antd';
import { storeState } from './utils';
const msgpack = require('msgpack-lite');

const CheckboxGroup = Checkbox.Group;


import { Radio } from 'antd';

const RadioGroup = Radio.Group;

class App extends React.Component {
  state = {
    value: 1,
  }

  onChange = (e) => {
    console.log('radio checked', e.target.value);
    this.setState({
      value: e.target.value,
    });
  }

  render() {
    return (
      <RadioGroup onChange={this.onChange} value={this.state.value}>
        <Radio value={1}>A</Radio>
        <Radio value={2}>B</Radio>
        <Radio value={3}>C</Radio>
        <Radio value={4}>D</Radio>
      </RadioGroup>
    );
  }
}

ReactDOM.render(<App />, mountNode);





// function onChange(checkedValues) {
//   console.log('checked = ', checkedValues);
// }

const plainOptions = ['Apple', 'Pear', 'Orange'];
const options = [
  { label: 'Apple', value: 'Apple' },
  { label: 'Pear', value: 'Pear' },
  { label: 'Orange', value: 'Orange' },
];
const optionsWithDisabled = [
  { label: 'Apple', value: 'Apple' },
  { label: 'Pear', value: 'Pear' },
  { label: 'Orange', value: 'Orange', disabled: false },
];

ReactDOM.render(
  <div>
    <CheckboxGroup options={plainOptions} defaultValue={['Apple']} onChange={onChange} />
    <br /><br />
    <br /><br />
    <CheckboxGroup options={optionsWithDisabled} disabled defaultValue={['Apple']} onChange={onChange} />
  </div>,
  mountNode);

export default class Checkboxes extends React.Component {
    constructor(props) {
        super(props);
        var local = sessionStorage.getItem(this.props.uuid);
        if (local === null) {
            this.state = {value: this.props.default, options: this.props.initOptions};
        } else {
            this.state = JSON.parse(local);
        }
    }

    handleChange = value => {
        this.setState({value: value});
        this.props.socket.emit(this.props.uuid + '#change', msgpack.encode(value));
        storeState(this.props.uuid, this.state, {value: value});
    }

    choose = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({value: arr});
        storeState(this.props.uuid, this.state, {value: arr});
    }

    newOptions = data => {
        var arr = new Uint8Array(data['data']);
        this.setState({value: null, options: msgpack.decode(arr)});
        storeState(this.props.uuid, this.state, {value: null, options: msgpack.decode(arr)});
    }

    componentDidMount() {
        var socket = this.props.socket;
        var uuid = this.props.uuid;
        socket.on(uuid + '#get', this.getValue);
        socket.on(uuid + '#options', this.newOptions);
        socket.on(uuid + '#choose', this.choose);
    }

    getValue = (data, fn) => {
        fn(msgpack.encode(this.state.value));
    }

    render () {
        return (
            // <Select
            //     multi={this.props.multi}
            //     value={this.state.value}
            //     options={this.state.options}
            //     onChange={this.handleChange}
            // />
            <CheckboxGroup options={options} defaultValue={['Pear']} onChange={this.handleChange} />
        );
    }
}

Checkboxes.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    multi: PropTypes.bool.isRequired,
    default: PropTypes.any,
    initOptions: PropTypes.array
};
