import pytest
from bs4 import BeautifulSoup

from ogpy import types
from ogpy.parser import parse


@pytest.mark.parametrize(
    "html,len_images",
    [
        pytest.param(
            """
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
            """,
            1,
            id="single-image",
        ),
        pytest.param(
            """
                <html>
                    <head>
                        <meta property="og:title" content="EXAMPLE">
                        <meta property="og:type" content="website">
                        <meta property="og:url" content="http://example.com">
                        <meta property="og:image" content="http://example.com/example.jpg">
                        <meta property="og:image" content="http://example.com/example.png">
                    </head>
                    <body>
                    </body>
                </html>
            """,
            2,
            id="multiple-image",
        ),
        pytest.param(
            """
                <html>
                    <head>
                        <meta property="og:title" content="EXAMPLE">
                        <meta property="og:type" content="website">
                        <meta property="og:url" content="http://example.com">
                        <meta property="og:image" content="http://example.com/example.jpg">
                        <meta property="og:image:width" content="480">
                    </head>
                    <body>
                    </body>
                </html>
            """,
            1,
            id="single-image-with-attributes",
        ),
        pytest.param(
            """
                <html>
                    <head>
                        <meta property="og:title" content="EXAMPLE">
                        <meta property="og:type" content="website">
                        <meta property="og:url" content="http://example.com">
                        <meta property="og:image" content="http://example.com/example.jpg">
                        <meta property="og:image" content="http://example.com/example.png">
                        <meta property="og:image:width" content="480">
                    </head>
                    <body>
                    </body>
                </html>
            """,
            2,
            id="multiple-image-with-attributes",
        ),
    ],
)
def test_simple_content(html, len_images):
    soup = BeautifulSoup(html, "html.parser")
    metadata = parse(soup)
    assert isinstance(metadata, types.Metadata)
    assert len(metadata.images) == len_images


def test_attribute_types():
    pass
    html = """
        <html>
            <head>
                <meta property="og:title" content="EXAMPLE">
                <meta property="og:type" content="website">
                <meta property="og:url" content="http://example.com">
                <meta property="og:image" content="http://example.com/example.jpg">
                <meta property="og:image:type" content="image/jpeg">
                <meta property="og:image:width" content="400">
                <meta property="og:image:height" content="300">
            </head>
            <body>
            </body>
        </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    metadata = parse(soup)
    assert isinstance(metadata, types.Metadata)
    assert isinstance(metadata.images[0].width, int)
    assert isinstance(metadata.images[0].height, int)
    assert isinstance(metadata.images[0].type, str)
    assert metadata.images[0].alt is None
