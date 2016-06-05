#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
import eventlet
from eventlet.queue import LightQueue

import dill as pickle

app = Flask(__name__)
app.debug = {{ debug|default(False) }}
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

{% for component in components %}
{{ "queue_" ~ component.name ~ "_" ~ component.uuid }} = LightQueue()

@socketio.on('{{component.uuid ~ "#put"}}')
def {{"get_" ~ component.name ~ "_" ~ component.uuid}}(data):
    print('got sometingsss')
    {{ "queue_" ~ component.name ~ "_" ~ component.uuid }}.put(data)

{% endfor %}

# {% for subscription in subscriptions %}
# socketio.on({{ subscription.event }})(
#     pickle.loads({{ subscription.func }})
# )
# {% endfor %}

# OLD SEPARATE
#
# {% for subscription in subscriptions %}
# foo = pickle.loads({{ subscription.func }})
# #     {% for component in components %}
# # foo.__globals__['{{ "queue_" ~ component.name ~ "_" ~ component.uuid }}'] = {{ "queue_" ~ component.name ~ "_" ~ component.uuid }}
# #     {% endfor %}
# socketio.on({{ subscription.event }})(foo)
# {% endfor %}
#
# {% for function in functions %}
# {{ function.name }} = pickle.loads({{ function.string }})
# {% endfor %}

from flask import copy_current_request_context

{% for subscription in subscriptions %}
@socketio.on({{ subscription.event }})
def zzz(x):
    print(x)
    foo = copy_current_request_context(pickle.loads({{ subscription.func }}))
    eventlet.spawn(foo, x)
{% endfor %}

if __name__ == '__main__':
    socketio.run(app, host={{ host }}, port={{ port }})
