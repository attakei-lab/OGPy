import pytest

from ogpy.client import browser


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
    metadata = browser.fetch(url)
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


@pytest.mark.webtest
@pytest.mark.xfail(reason="Respons is 403")
def test_fetch_real_online_content():
    """This case requests IMDB website that is used as example in OGP website."""
    data = browser.fetch("https://www.imdb.com/title/tt0117500/")
    assert data.title == "The Rock (1996) ⭐ 7.4 | Action, Adventure, Thriller"
    assert data.type == "video.movie"
    assert data.url == "https://www.imdb.com/title/tt0117500/"
    assert (
        data.images[0].url
        == "https://m.media-amazon.com/images/M/MV5BMDhkYjRiZWEtZTE0Ny00ZjA1LThmNjgtM2UyYTQzODA4MjdhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg"
    )


@pytest.mark.webtest
def test_fetch__wait_javascript_challenge():
    """This case requests IMDB website that is used as example in OGP website."""
    data = browser.fetch("https://pypi.org/project/sphinx-revealjs")
    assert data.title == "sphinx-revealjs"
    assert data.type == "website"
    assert data.url == "https://pypi.org/project/sphinx-revealjs/"


@pytest.mark.webtest
def test_fetch__with_installing_browser():
    """This case requests IMDB website that is used as example in OGP website."""
    data = browser.fetch(
        "https://pypi.org/project/sphinx-revealjs", browser_name="firefox"
    )
    assert data.title == "sphinx-revealjs"
    assert data.type == "website"
    assert data.url == "https://pypi.org/project/sphinx-revealjs/"


@pytest.mark.webtest
def test_fetch_for_cache__cachable():
    metadata, expired_at = browser.fetch_for_cache("https://ogp.me/")
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
    assert expired_at
