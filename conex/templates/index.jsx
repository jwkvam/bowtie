import 'normalize.css';
import React from 'react';
import {render} from 'react-dom';
import io from 'socket.io-client';

{% for component in components %}
import {{ component.component }} from './{{ component.module }}';
{% endfor %}

var socket = io();

class Dashboard extends React.Component {
    render() {
        return (
            <div style={{ '{{' }}display: 'flex', flexFlow: 'row nowrap'{{ '}}' }}>
                <div style={{ '{{' }}display: 'flex', flexDirection: 'column', flex: 1{{ '}}' }}>
                    {% for control in controls %}
                    {{ control }}
                    {% endfor %}

                </div>
                <div style={{ '{{' }}display: 'flex', flexDirection: 'column', flex: 9{{ '}}' }}>

                    {% for visualrow in visuals %}
                    <div style={{ '{{' }}display: 'flex', flexFlow: 'row nowrap'{{ '}}' }}>
                        {% for visual in visualrow %}
                        {{ visual }}
                        {% endfor %}
                    </div>
                    {% endfor %}
                </div>
            </div>
        );
    }
}

render(<Dashboard />, document.getElementById('app'));
