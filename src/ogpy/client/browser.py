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
"""Browser type category of Playwright."""
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
"""Chromium channel category of Playwright."""
BrowserLabel = BrowserName | BrowserChannel
"""Combined types that is accepted by functions."""


def get_browser(playwright: Playwright, name: BrowserLabel) -> Browser:
    """Retrieve browser instance of Playwright.

    This function works these automatically.

    * Detect browser 'type' or 'channel'.
    * Download executable if it is not installed yet.

    :param playwright: Playwright object.
    :param name: Target browser for using.
    """
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
    """Low-level class to fetch Open Graph metadata by Browser."""

    def __init__(
        self,
        playwright: Playwright,
        fuzzy_mode: bool = False,
        browser_name: BrowserLabel = "chromium",
    ):
        """Initialize engine.

        This class must be created in Playwright context.

        .. code:: python

           with sync_playwright() as p:
               engine = Engine(p)

        :param playwright: Running Playwright object.
        :param fuzzy_mode: Flag to enable "Fuzzy mode", See :ref:`fuzzy-mode`.
        :param browser_name: Using browser.
        """
        self._playwright = playwright
        self._fuzzy_mode = fuzzy_mode
        self._browser = get_browser(self._playwright, browser_name)

    def fetch_for_cache(
        self, url: str
    ) -> Tuple[types.Metadata | types.MetadataFuzzy, int]:
        """Fetch and parse HTTP content. return with max-age for caching.

        :param url: Target URL.
        :returns: Fetched meatadata and cachable max-age (seconds).
        """
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
        """Fetch and parse HTTP content.

        :param url: Target URL.
        :returns: Fetched meatadata.
        """
        metadata, _ = self.fetch_for_cache(url)
        return metadata


def fetch(
    url: str,
    fuzzy_mode: bool = False,
    browser_name: BrowserLabel = "chromium",
) -> types.Metadata | types.MetadataFuzzy:
    """Fetch and parse HTTP content.

    :param url: Target URL.
    :param fuzzy_mode: Flag to enable "Fuzzy mode", See :ref:`fuzzy-mode`.
    :param browser_name: Using browser.
    :returns: Fetched meatadata.
    """
    with sync_playwright() as p:
        engine = Engine(p, fuzzy_mode, browser_name)
        return engine.fetch(url)


def fetch_for_cache(
    url: str,
    fuzzy_mode: bool = False,
    browser_name: BrowserLabel = "chromium",
) -> Tuple[types.Metadata | types.MetadataFuzzy, int | None]:
    """Fetch and parse HTTP content. return with max-age for caching.

    :param url: Target URL.
    :param fuzzy_mode: Flag to enable "Fuzzy mode", See :ref:`fuzzy-mode`.
    :param browser_name: Using browser.
    :returns: Fetched meatadata and cachable max-age (seconds).
    """
    with sync_playwright() as p:
        engine = Engine(p, fuzzy_mode, browser_name)
        return engine.fetch_for_cache(url)
