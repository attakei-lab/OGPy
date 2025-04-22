"""Browser based client.

This module provide functions as same as :py:class:`ogpy.client`.
Functions uses Playwright and browser instead of httpx.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from .. import parser, types

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Playwright


def get_browser(playwright: Playwright, name: str) -> Browser:
    if not hasattr(playwright, name):
        raise ValueError(f"Browser type '{name}' is not supported.")
    return playwright.chromium.launch(channel=name)


def fetch(
    url: str,
    fuzzy_mode: bool = False,
    browser_name: str = "chromium",
) -> types.Metadata | types.MetadataFuzzy:
    """Fetch and parse HTTP content."""
    with sync_playwright() as p:
        browser = get_browser(p, browser_name)
        page = browser.new_page()
        resp = page.goto(url, wait_until="networkidle")
        if not resp:
            raise Exception("Response is `None`.")
        if not resp.ok:
            raise Exception(f"Response status is {resp.status} {resp.status_text}")
        print(page.content())
        soup = BeautifulSoup(page.content(), "html.parser")
    return parser.parse(soup, fuzzy_mode)
