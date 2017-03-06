import 'normalize.css';
import React from 'react';
import {render} from 'react-dom';
import io from 'socket.io-client';
import 'antd/dist/antd.css'

import CProgress from './progress';

{% for component in components %}
import {{ component.component }} from './{{ component.module }}';
{% endfor %}

var msgpack = require('msgpack-lite');
var socket = io();

class Dashboard extends React.Component {
    constructor(props) {
        super(props);
        this.cache = {};
        socket.emit('INITIALIZE');
    }

    saveValue = data => {
        var arr = new Uint8Array(data['data']);
        var keyvalue = msgpack.decode(arr);
        this.cache[keyvalue[0]] = keyvalue[1];
    }

    loadValue = (data, fn) => {
        var arr = new Uint8Array(data['data']);
        var key = msgpack.decode(arr);
        fn(msgpack.encode(this.cache[key]));
    }

    componentDidMount() {
        socket.on('cache_save', this.saveValue);
        socket.on('cache_load', this.loadValue);
    }

    render() {
        return (
            <div style={{ '{{' }}display: 'flex', flexFlow: 'row nowrap', width: '100%', height: '100%',
                    minHeight: '100vh', maxHeight: '100%',
                    minWidth: '100vw', maxWidth: '100%'{{ '}}' }}>
                <div style={{ '{{' }}display: 'flex', flexFlow: 'column nowrap', flex: '0 0 18em', padding: '7px', backgroundColor: '{{background_color}}'{{ '}}' }}>
                    {{ description }}

                    {% for control in controls %}
                    <div style={{ '{{' }}paddingBottom: '3px'{{ '}}' }}>
                    {{ control.caption }}
                    </div>

                    <div style={{ '{{' }}paddingBottom: '7px'{{ '}}' }}>
                    {{ control.instantiate }}
                    </div>
                    {% endfor %}
                </div>

                <div style={{ '{{' }}display: 'flex', flexFlow: 'column nowrap', flex: '1 1 0'{{ '}}' }}>
                    {% for visualrow, min_height in visuals %}
                    <div style={{ '{{' }}display: 'flex', minHeight: '{{ min_height }}px',
                            flexFlow: 'row nowrap', flex: '1 1 0'{{ '}}' }}>
                        {% for visual, progress, min_width in visualrow %}
                        <div style={{ '{{' }}display: 'flex', minWidth: '{{ min_width }}px',
                                flex: '1 1 0'{{ '}}' }}>
                            {{ progress }}
                            {{ visual }}
                            </CProgress>
                        </div>
                        {% endfor %}
                    </div>
                    {% endfor %}
                </div>
            </div>
        );
    }
}

render(<Dashboard />, document.getElementById('app'));
