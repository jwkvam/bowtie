import React from 'react';
import {render} from 'react-dom';
import { Flex, Item } from 'react-flex';
import io from 'socket.io-client';

var socket = io();

{% for component in components %}
{{ component }}
{% endfor %}


class Dashboard extends React.Component {
    render() {
        return (
            <Flex row>
                <Item flex={2}>
                    {% for control in controls %}
                    {{ control }}
                    {% endfor %}
                </Item>
                <Flex column>

                    {% for visualrow in visuals %}
                    <Flex row>
                        {% for visual in visualrow %}
                        <Item>
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
