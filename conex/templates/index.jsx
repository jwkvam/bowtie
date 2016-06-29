import 'react-flex/index.css';
import React from 'react';
import {render} from 'react-dom';
import { Flex, Item } from 'react-flex';
import io from 'socket.io-client';

{% for component in components %}
import {{ component.component }} from './{{ component.module }}';
{% endfor %}

var socket = io();

class Dashboard extends React.Component {
    render() {
        return (
            <Flex row>
                <Item flex={1}>
                    {% for control in controls %}
                    {{ control }}
                    {% endfor %}
                </Item>
                <Flex column flex={9}>

                    {% for visualrow in visuals %}
                    <Flex row flex={1} display='inline-flex'>
                        {% for visual in visualrow %}
                        <Item flex={1}>
                            {{ visual }}
                        </Item>
                        {% endfor %}
                    </Flex>
                    {% endfor %}
                </Flex>
            </Flex>
        );
    }
}

render(<Dashboard />, document.getElementById('app'));
