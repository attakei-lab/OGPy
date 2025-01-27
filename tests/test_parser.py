from bs4 import BeautifulSoup

from ogpy import types
from ogpy.parser import parse


def test_simple_content():
    html = """
        <html>
            <head>
                <meta property="og:title" content="EXAMPLE">
                <meta property="og:type" content="website">
                <meta property="og:url" content="http://example.com">
                <meta property="og:image" content="http://example.com/example.jpg">
            </head>
            <body>
            </body>
        </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    metadata = parse(soup)
    assert isinstance(metadata, types.Metadata)
