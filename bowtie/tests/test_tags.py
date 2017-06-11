# -*- coding: utf-8 -*-
"""Test tag instantation for components."""

from bowtie.visual import Markdown


def test_markdown():
    """Test tags for the Markdown widget."""
    # pylint: disable=protected-access
    next_uuid = Markdown._NEXT_UUID
    mark = Markdown()
    assert mark._instantiate == ("<AntProgress socket={{socket}} uuid={{'{next_uuid}'}}>"
                                 "<Markdown initial={{''}} "
                                 "socket={{socket}} uuid={{'{next_uuid1}'}} />"
                                 "</AntProgress>").format(next_uuid=next_uuid + 1,
                                                          next_uuid1=next_uuid + 2)

    next_uuid = Markdown._NEXT_UUID
    mark = Markdown(initial='#hi\n##hello')
    assert mark._instantiate == ("<AntProgress socket={{socket}} uuid={{'{next_uuid}'}}>"
                                 "<Markdown initial={{'<h1>hi</h1>\\n<h2>hello</h2>'}} "
                                 "socket={{socket}} uuid={{'{next_uuid1}'}} />"
                                 "</AntProgress>").format(next_uuid=next_uuid + 1,
                                                          next_uuid1=next_uuid + 2)
