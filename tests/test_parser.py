import pytest
from bs4 import BeautifulSoup

from ogpy import types
from ogpy.parser import parse


@pytest.mark.parametrize(
    "html,expected",
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
            {"len_images": 1, "audio": None},
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
            {"len_images": 2, "audio": None},
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
            {"len_images": 1, "audio": None},
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
            {"len_images": 2, "audio": None},
            id="multiple-image-with-attributes",
        ),
        pytest.param(
            """
                <html>
                    <head>
                        <meta property="og:title" content="EXAMPLE">
                        <meta property="og:type" content="website">
                        <meta property="og:url" content="http://example.com">
                        <meta property="og:image" content="http://example.com/example.jpg">
                        <meta property="og:audio" content="http://example.com/example.mp3">
                    </head>
                    <body>
                    </body>
                </html>
            """,
            {"len_images": 1, "audio": "http://example.com/example.mp3"},
            id="with-audio",
        ),
        pytest.param(
            """
                <html>
                    <head>
                        <meta property="og:title" content="EXAMPLE">
                        <meta property="og:type" content="website">
                        <meta property="og:url" content="http://example.com">
                        <meta property="og:image" content="http://example.com/example.jpg">
                        <meta property="og:locale:alternate" content="ja_JP">
                        <meta property="og:locale:alternate" content="fr_FR">
                    </head>
                    <body>
                    </body>
                </html>
            """,
            {
                "len_images": 1,
                "audio": None,
                "len_locale_alternates": 2,
            },
            id="with-audio",
        ),
    ],
)
def test_simple_content(html, expected):
    soup = BeautifulSoup(html, "html.parser")
    metadata = parse(soup)
    assert isinstance(metadata, types.Metadata)
    assert len(metadata.images) == expected["len_images"]
    assert metadata.audio == expected["audio"]
    if "len_locale_alternates" in expected:
        assert len(metadata.locale_alternates) == expected["len_locale_alternates"]


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


@pytest.mark.parametrize(
    "html,expected",
    [
        pytest.param("<html></html>", ValueError, id="no-head"),
        pytest.param("<htm><head></head></html>", TypeError, id="no-properties"),
        pytest.param(
            """
            <htm><head>
                <meta property="og:title" content="EXAMPLE">
            </head></html>
            """,
            TypeError,
            id="less-attributes",
        ),
        pytest.param(
            """
            <htm><head>
                <meta property="og:title" content="EXAMPLE">
                <meta property="og:type" content="website">
                <meta property="og:url" content="http://example.com">
                <meta property="og:image" content="http://example.com/example.jpg">
                <meta property="og:image:width" content="full">
            </head></html>
            """,
            ValueError,
            id="invalid-width",
        ),
        pytest.param(
            """
            <htm><head>
                <meta property="og:title" content="EXAMPLE">
                <meta property="og:type" content="website">
                <meta property="og:url" content="http://example.com">
                <meta property="og:image" content="http://example.com/example.jpg">
                <meta property="og:determiner" content="them" >
            </head></html>
            """,
            ValueError,
            id="invalid-determiner",
        ),
    ],
)
def test_parse_errors_with_strict(html, expected):
    soup = BeautifulSoup(html, "html.parser")
    with pytest.raises(expected):
        parse(soup, False)


@pytest.mark.parametrize(
    "html,expected",
    [
        pytest.param("<htm><head></head></html>", TypeError, id="no-properties"),
        pytest.param(
            """
            <htm><head>
                <meta property="og:title" content="EXAMPLE">
            </head></html>
            """,
            TypeError,
            id="less-attributes",
        ),
    ],
)
def test_parse_success_when_fuzzy(html, expected):
    soup = BeautifulSoup(html, "html.parser")
    parse(soup, True)  # Not raise error
