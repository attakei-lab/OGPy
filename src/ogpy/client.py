"""HTTP client wrapper."""

import re
from datetime import datetime
from typing import Tuple

import httpx
from bs4 import BeautifulSoup

from . import types, parser, __version__

USER_AGENT = f"OGPy client v{__version__}"


def fetch(url: str, fuzzy_mode: bool = False) -> types.Metadata | types.MetadataFuzzy:
    """Fetch and parse HTTP content."""
    resp = httpx.get(url, headers={"user-agent": USER_AGENT}, follow_redirects=True)
    if not resp.is_success:
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return parser.parse(soup, fuzzy_mode)


def fetch_for_cache(
    url: str, fuzzy_mode: bool = False
) -> Tuple[types.Metadata | types.MetadataFuzzy, int | None]:
    """Fetch and parse HTTP content. return with max-age for caching."""
    now = datetime.now()
    resp = httpx.get(url, headers={"user-agent": USER_AGENT}, follow_redirects=True)
    if not resp.is_success:
        resp.raise_for_status()
    max_age = None
    if "cache-control" in resp.headers:
        parts = re.split(r",\s+", resp.headers["cache-control"])
        values = dict([v.split("=") for v in parts if "=" in v])
        max_age = int(now.timestamp()) + int(values.get("max-age", 0))
        if "age" in resp.headers:
            max_age -= int(resp.headers["age"])
    soup = BeautifulSoup(resp.text, "html.parser")
    return parser.parse(soup, fuzzy_mode), max_age
