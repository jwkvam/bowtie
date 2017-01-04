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
