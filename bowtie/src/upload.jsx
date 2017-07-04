import React from 'react';
import PropTypes from 'prop-types';
import { Upload, Icon, message } from 'antd';
import 'antd/dist/antd.css';

const Dragger = Upload.Dragger;

export default class AntUpload extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <Dragger action={'upload' + this.props.uuid}>
                <p className="ant-upload-drag-icon">
                    <Icon type="inbox" />
                </p>
                <p className="ant-upload-text">Click or drag file to this area to upload</p>
                <p className="ant-upload-hint">Support for a single or bulk upload.</p>
            </Dragger>
        );
    }
}

AntUpload.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
};
