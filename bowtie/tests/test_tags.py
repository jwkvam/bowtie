"""Test tag instantation for components."""

from bowtie.html import Markdown


def test_markdown():
    """Test tags for the Markdown widget."""
    # pylint: disable=protected-access
    next_uuid = Markdown._NEXT_UUID
    mark = Markdown()
    assert mark._instantiate == (
        f"<Markdown initial={{''}} socket={{socket}} uuid={{'{next_uuid + 1}'}} />"
    )

    next_uuid = Markdown._NEXT_UUID
    mark = Markdown(initial='#hi\n##hello')
    assert mark._instantiate == (
        "<Markdown initial={'<h1>hi</h1>\\n<h2>hello</h2>'} "
        f"socket={{socket}} uuid={{'{next_uuid + 1}'}} />"
    )
