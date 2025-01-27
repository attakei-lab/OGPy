"""Parse functions."""

from typing import Any, Callable

from bs4 import BeautifulSoup

from . import types


def _determiner(val: str) -> str:
    if val not in ["a", "an", "the", "", "auto"]:
        raise ValueError("determiner must be one of 'a', 'an', 'the', '' and 'auto'.")
    return val


def parse_type(name) -> Callable:
    """Resolve type of propety."""
    if name in ["width", "height"]:
        return int
    if name == "determiner":
        return _determiner
    return str


def parse(soup: BeautifulSoup) -> types.Metadata:
    """Parse ogp properties as object from BeautifulSoup."""
    props: dict[str, Any] = {}
    if not soup.head:
        raise ValueError("<head> tag is not exists.")
    for meta in soup.head.find_all("meta"):
        if not ("property" in meta.attrs and "content" in meta.attrs):
            continue
        if not meta["property"].startswith("og:"):
            continue
        prop = meta["property"][3:]
        # image and attributes
        if prop == "image":
            props.setdefault("images", [])
            props["images"].append(types.ImageMetadata(url=meta["content"]))
            continue
        if prop.startswith("image:"):
            prop = prop[6:]
            setattr(props["images"][0], prop, parse_type(prop)(meta["content"]))
            continue
        # locale_alternates
        if prop == "locale:alternate":
            props.setdefault("locale_alternates", [])
            props["locale_alternates"].append(meta["content"])
            continue
        # Other properties
        props[prop] = parse_type(prop)(meta["content"])
    return types.Metadata(**props)
