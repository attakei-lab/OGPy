import pytest

from ogpy import client


@pytest.mark.webtest
@pytest.mark.parametrize(
    "url",
    [
        pytest.param("http://ogp.me", id="http-unslashed"),
        pytest.param("http://ogp.me/", id="http-slashed"),
        pytest.param("https://ogp.me", id="https-unslashed"),
        pytest.param("https://ogp.me/", id="https-slashed"),
    ],
)
def test_fetch_online_content(url):
    metadata = client.fetch(url)
    assert metadata.title == "Open Graph protocol"
    assert metadata.type == "website"
    assert metadata.url == "https://ogp.me/"
    assert (
        metadata.description
        == "The Open Graph protocol enables any web page to become a rich object in a social graph."
    )
    assert len(metadata.images) == 1
    image = metadata.images[0]
    assert image.url == "https://ogp.me/logo.png"
    assert image.width == 300
    assert image.height == 300
    assert image.alt == "The Open Graph logo"
