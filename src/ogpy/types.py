"""Type definitions.

Refs
----

* https://ogp.me/
"""

from dataclasses import dataclass, field
from typing import Literal


DETERMINER = Literal["a", "an", "the", "", "auto"]
NUMBER = int | float


@dataclass
class ImageMetadata:
    """Image property structure.

    :ref: https://ogp.me/#structured
    """

    url: str
    secure_url: str | None = None
    type: str | None = None
    width: NUMBER | None = None
    height: NUMBER | None = None
    alt: str | None = None


@dataclass
class Metadata:
    """Open Graph metadata structure.

    :ref: https://ogp.me/#metadata
    """

    # Basic metadata
    title: str
    type: str
    url: str
    images: list[ImageMetadata]
    # Optional metadata
    audio: str | None = None
    description: str | None = None
    determiner: DETERMINER = ""
    locale: str = "en_US"
    locale_alternates: list[str] = field(default_factory=list)
    site_name: str | None = None
    video: str | None = None
