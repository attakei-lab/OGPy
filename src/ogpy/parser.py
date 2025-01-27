"""Parse functions."""

from typing import Any

from bs4 import BeautifulSoup

from . import types


def parse_type(name):
    if name in ["width", "height"]:
        return int
    return str


def parse(soup: BeautifulSoup) -> types.Metadata:
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
        # Other properties
        props[prop] = meta["content"]
    return types.Metadata(**props)
