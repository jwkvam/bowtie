import 'normalize.css';
import React from 'react';
import {render} from 'react-dom';
import io from 'socket.io-client';
import 'antd/dist/antd.css'

import CProgress from './progress';

{% for component in components %}
import {{ component.component }} from './{{ component.module }}';
{% endfor %}

var socket = io();

class Dashboard extends React.Component {
    constructor(props) {
        super(props);
        socket.emit('INITIALIZE');
    }

    render() {
        return (
            <div style={{ '{{' }}display: 'flex', flexFlow: 'row nowrap', width: '100vw', height: '100vh', maxHeight: '100%', maxWidth: '100%'{{ '}}' }}>
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
                    {% for visualrow in visuals %}
                    <div style={{ '{{' }}display: 'flex', flexFlow: 'row nowrap', flex: '1 1 0'{{ '}}' }}>
                        {% for visual, progress in visualrow %}
                        <div style={{ '{{' }}display: 'flex', flex: '1 1 0'{{ '}}' }}>
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
