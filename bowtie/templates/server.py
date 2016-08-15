#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import click
from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, emit
import eventlet

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import {{source_module}}

app = Flask(__name__)
app.debug = {{ debug|default(False) }}
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

{% for event, functions in subscriptions.items() %}
@socketio.on({{ event }})
def _(*args):
    {% for func in functions %}
    foo = copy_current_request_context({{ source_module }}.{{ func }})
    eventlet.spawn(foo, *args)
    {% endfor %}
{% endfor %}

@click.command()
@click.option('--host', '-h', default={{host}}, help='Host IP')
@click.option('--port', '-p', default={{port}}, help='port number')
def main(host, port):
    socketio.run(app, host=host, port=port)

if __name__ == '__main__':
    main()
