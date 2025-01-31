from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp
from sphinx.testing.path import path

test_root = Path(__file__).parents[1]


@pytest.fixture(scope="module")
def rootdir():
    """Set root directory to use testing sphinx project."""
    return path(test_root / "roots")


@pytest.mark.webtest
@pytest.mark.sphinx("html", testroot="default")
def test_href(app: SphinxTestApp, status, warning):  # noqa
    app.build()
    html_path = Path(app.outdir) / "index.html"
    soup = BeautifulSoup(html_path.read_text(), "html.parser")
    a = soup.find_all("a", {"href": "http://ogp.me/"})
    assert a
    assert a[0].img["src"] == "https://ogp.me/logo.png"
