#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bowtie.control import Nouislider, DropDown, Button
from bowtie.visual import Plotly, Table, SmartGrid

import numpy as np
import numpy.random as rng
import json
import plotlywrapper as pw

slide = Nouislider()
slide2 = Nouislider()
butt = Button(label='Clicker')
ddown = DropDown(name='hello', options=list(range(5)))

plot = Plotly()
plot2 = Plotly()
plot3 = Plotly()
table1 = SmartGrid()

def newtable():
    print('hello')
    X = rng.randn(100, 2)
    data = []
    for x in X:
        data.append(dict(ab=x[0], ba=x[1]))
    table1.do_update(data)

def foo(x):
    t = np.linspace(0, 1, 10);
    # x = slide2.value
    y = slide2.get()
    print(y)

    figure = pw.line(t, float(y) * np.sin(float(x[0]) * t))
    figure.layout['autosize'] = True
    # figure.layout['height'] = 700
    plot.do_all(figure.to_json())
    print('finish foo')

def foo2(y):
    t = np.linspace(0, 1, 10);
    # x = slide2.value
    x = slide.get()
    plot2.do_all(pw.line(t, y['y'] * np.sin(float(x) * t)).to_json())


def foo3(dd):
    t = np.linspace(0, 1, 10);
    # x = slide2.value
    dd = ddown.get()
    # print('ddown value: {}'.format(dd))
    # x = slide.get()
    plot3.do_all(pw.line(t, t * dd['value']).to_json())


if __name__ == "__main__":

    from bowtie import Layout
    layout = Layout()
    layout.add_controller(slide)
    layout.add_controller(slide2)
    layout.add_controller(ddown)
    layout.add_controller(butt)
    layout.add_visual(plot)
    layout.add_visual(plot2, next_row=True)
    layout.add_visual(plot3)
    layout.add_visual(table1)

    layout.subscribe(butt.on_click, newtable)
    layout.subscribe(slide.on_change, foo)
    layout.subscribe(plot.on_click, foo2)
    layout.subscribe(ddown.on_change, foo3)

    layout.build(debug=False)
