#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example Bowtie App.
"""

from bowtie.control import Nouislider
from bowtie.visual import Plotly

import numpy as np
from numpy import random as rng
import plotlywrapper as pw


sigma = Nouislider(caption='Sigma', start=1, minimum=0.1, maximum=50)
mainplot = Plotly()

data = np.zeros(100).tolist()


def walk():
    value = float(sigma.get())
    data.pop(0)
    data.append(value * rng.randn() + data[-1])
    mainplot.do_all(pw.line(data).to_json())


if __name__ == "__main__":
    from bowtie import Layout
    layout = Layout(debug=False)
    layout.add_controller(sigma)
    layout.add_visual(mainplot)
    layout.schedule(0.1, walk)

    layout.build()
