"""Type definitions.

Refs
----

* https://ogp.me/
"""

from dataclasses import KW_ONLY, dataclass, field
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
class _OptionalMetadata:
    """Optional properties of protocol.

    :ref: https://ogp.me/#optional
    """

    _: KW_ONLY  # NOTE: To inherit
    audio: str | None = None
    description: str | None = None
    determiner: DETERMINER = ""
    locale: str = "en_US"
    locale_alternates: list[str] = field(default_factory=list)
    site_name: str | None = None
    video: str | None = None


@dataclass
class Metadata(_OptionalMetadata):
    """Open Graph metadata structure.

    This class raises error when content don't have required properties.

    :ref: https://ogp.me/#metadata
    """

    title: str
    type: str
    url: str
    images: list[ImageMetadata]


@dataclass
class MetadataFuzzy(_OptionalMetadata):
    """Open Graph metadata structure.

    This class does not raise error if content don't have any properties.

    :ref: https://ogp.me/#metadata
    """

    title: str | None = None
    type: str | None = None
    url: str | None = None
    images: list[ImageMetadata] = field(default_factory=list)
