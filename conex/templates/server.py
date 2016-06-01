#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

import dill as pickle

app = Flask(__name__)
app.debug = {{ debug|default(False) }}
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

{% for subscription in subscriptions %}
socketio.on({{ subscription.event }})(
    pickle.loads({{ subscription.func }})
)
{% endfor %}

if __name__ == '__main__':
    socketio.run(app, host={{ host }}, port={{ port }})
