"""HTTP client wrapper."""

import httpx
from bs4 import BeautifulSoup

from . import types, parser, __version__

USER_AGENT = f"OGPy client v{__version__}"


def fetch(url: str, strict: bool = False) -> types.Metadata | types.MetadataStrict:
    """Fetch and parse HTTP content."""
    resp = httpx.get(url, headers={"user-agent": USER_AGENT}, follow_redirects=True)
    if not resp.is_success:
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return parser.parse(soup, strict)
