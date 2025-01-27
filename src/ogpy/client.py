"""HTTP client wrapper."""

import httpx
from bs4 import BeautifulSoup

from . import types, parser


def fetch(url: str) -> types.Metadata:
    """Fetch and parse HTTP content."""
    resp = httpx.get(url, allow_redirects=True)
    soup = BeautifulSoup(resp.text, "html.parser")
    return parser.parse(soup)
