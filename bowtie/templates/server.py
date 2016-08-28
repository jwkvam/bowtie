#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import traceback

import click
from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, emit
import eventlet

# import the user created module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import {{source_module}}

app = Flask(__name__)
app.debug = {{ debug|default(False) }}
socketio = SocketIO(app)

def context(func):
    def foo():
        with app.app_context():
            func()
    return foo


class Scheduler(object):

    def __init__(self, seconds, func):
        self.seconds = seconds
        self.func = func
        self.thread = None

    def start(self):
        self.thread = eventlet.spawn(self.run)

    def run(self):
        ret = eventlet.spawn(context(self.func))
        eventlet.sleep(self.seconds)
        try:
            ret.wait()
        except:
            traceback.print_exc()
        self.thread = eventlet.spawn(self.run)

    def stop(self):
        if self.thread:
            self.thread.cancel()


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
    scheds = []
    {% for schedule in schedules %}
    sched = Scheduler({{ schedule.seconds }},
                      {{ source_module }}.{{ schedule.function }})
    scheds.append(sched)
    {% endfor %}

    for sched in scheds:
        sched.start()
    socketio.run(app, host=host, port=port)
    for sched in scheds:
        sched.stop()

if __name__ == '__main__':
    main()
