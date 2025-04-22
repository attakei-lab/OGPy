"""Browser based client.

This module provide functions as same as :py:class:`ogpy.client`.
Functions uses Playwright and browser instead of httpx.
"""

from __future__ import annotations

import logging
import re
import subprocess
from datetime import datetime
from typing import TYPE_CHECKING, Literal

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from .. import parser, types

if TYPE_CHECKING:
    from typing import Tuple

    from playwright.sync_api import Browser, Playwright

logger = logging.getLogger(__name__)

BrowserName = Literal["chromium", "firefox", "webkit"]
BrowserChannel = Literal[
    "chrome",
    "msedge",
    "chrome-beta",
    "msedge-beta",
    "chrome-dev",
    "msedge-dev",
    "chrome-canary",
    "msedge-canary",
]
BrowserLabel = BrowserName | BrowserChannel


def get_browser(playwright: Playwright, name: BrowserLabel) -> Browser:
    browser_name = "chromium"
    browser_channel = None
    if name in BrowserName.__args__:  # type: ignore[attr-defined]
        browser_name = name
    elif name in BrowserChannel.__args__:  # type: ignore[attr-defined]
        browser_channel = name
    else:
        raise ValueError(f"Browser type '{name}' is not supported.")

    # Install browser automatically.
    logger.info(f"Now installing browser '{name}' automatically.")
    subprocess.run(f"playwright install {name}".split())

    return getattr(playwright, browser_name).launch(channel=browser_channel)


class Engine:
    def __init__(
        self,
        playwright: Playwright,
        browser_name: BrowserLabel = "chromium",
        fuzzy_mode: bool = False,
    ):
        self._playwright = playwright
        self._browser = get_browser(self._playwright, browser_name)
        self._fuzzy_mode = fuzzy_mode

    def fetch_for_cache(
        self, url: str
    ) -> Tuple[types.Metadata | types.MetadataFuzzy, int]:
        """Fetch and parse HTTP content. return with max-age for caching."""
        now = datetime.now()
        max_age = int(now.timestamp())
        page = self._browser.new_page()
        resp = page.goto(url, wait_until="networkidle")
        if not resp:
            raise Exception("Response is `None`.")
        if not resp.ok:
            raise Exception(f"Response status is {resp.status} {resp.status_text}")
        soup = BeautifulSoup(page.content(), "html.parser")
        if "cache-control" in resp.headers:
            parts = re.split(r",\s+", resp.headers["cache-control"])
            values = dict([v.split("=") for v in parts if "=" in v])
            max_age = int(now.timestamp()) + int(values.get("max-age", 0))
            if "age" in resp.headers:
                max_age -= int(resp.headers["age"])
        return parser.parse(soup, self._fuzzy_mode), max_age

    def fetch(self, url: str) -> types.Metadata | types.MetadataFuzzy:
        """Fetch and parse HTTP content."""
        metadata, _ = self.fetch_for_cache(url)
        return metadata


def fetch(
    url: str,
    fuzzy_mode: bool = False,
    browser_name: BrowserLabel = "chromium",
) -> types.Metadata | types.MetadataFuzzy:
    """Fetch and parse HTTP content."""
    with sync_playwright() as p:
        engine = Engine(p, browser_name, fuzzy_mode)
        return engine.fetch(url)


def fetch_for_cache(
    url: str,
    fuzzy_mode: bool = False,
    browser_name: BrowserLabel = "chromium",
) -> Tuple[types.Metadata | types.MetadataFuzzy, int | None]:
    """Fetch and parse HTTP content. return with max-age for caching."""
    with sync_playwright() as p:
        engine = Engine(p, browser_name, fuzzy_mode)
        return engine.fetch_for_cache(url)
