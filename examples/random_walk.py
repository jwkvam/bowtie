#!/usr/bin/env python
"""Example Bowtie App."""

from bowtie.control import Nouislider
from bowtie.visual import Plotly
from bowtie import Pager, cache, command

import numpy as np
from numpy import random as rng
import plotlywrapper as pw


pager = Pager()
sigma = Nouislider(caption='Sigma', start=0., minimum=0.1, maximum=50.)
mainplot = Plotly()


def initialize():
    cache.save('data', [0.] * 100)


def upgraph():
    data = cache.load('data')
    value = float(sigma.get())
    data.pop(0)
    data.append(value * rng.randn() + data[-1])
    mainplot.do_all(pw.line(data).to_json())
    cache.save('data', data)


def walk():
    pager.notify()


@command
def main():
    from bowtie import App
    app = App(debug=True)
    app.add_sidebar(sigma)
    app.add(mainplot)
    app.schedule(0.1, walk)
    app.respond(pager, upgraph)
    return app
