import React from 'react';
import PropTypes from 'prop-types';
import { Upload, Icon, LocaleProvider } from 'antd';
import enUS from 'antd/lib/locale-provider/en_US';
import 'antd/dist/antd.css';

const Dragger = Upload.Dragger;

export default class AntUpload extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <LocaleProvider locale={enUS}>
                <Dragger
                    action={'upload' + this.props.uuid}
                    multiple={this.props.multiple} >
                    <p className="ant-upload-drag-icon">
                        <Icon type="inbox" />
                    </p>
                    <p className="ant-upload-text">Click or drag file to this area to upload</p>
                    <p className="ant-upload-hint">Support for a single or bulk upload.</p>
                </Dragger>
            </LocaleProvider>
        );
    }
}

AntUpload.propTypes = {
    uuid: PropTypes.string.isRequired,
    socket: PropTypes.object.isRequired,
    multiple: PropTypes.bool.isRequired,
};
