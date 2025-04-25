"""OGPy Sphinx adapter."""

from __future__ import annotations

import importlib.metadata
from datetime import datetime
from typing import TYPE_CHECKING

from docutils import nodes
from docutils.parsers.rst.directives.images import Figure, Image
from sphinx.domains import Domain
from sphinx.util.logging import getLogger

from ..client import fetch_for_cache

if TYPE_CHECKING:
    from typing import Tuple
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment

    from .. import types

logger = getLogger(__name__)


class OGPImageDirective(Image):
    """Extended directive for og-image.

    User pass content url as arguments instead of image url.
    In extension process, it converts from content to image.
    """

    option_spec = Image.option_spec.copy()
    del option_spec["target"]

    def run(self):  # noqa: D102
        self.options["target"] = self.arguments[0]
        nodeset = super().run()
        imageref = nodeset[-1]
        image = imageref[0] if imageref.children else imageref
        # Flag that image uri is set content URL, and fetch metadata by OgpDomain.
        image["mark-ogpy"] = True
        return nodeset


class OGPFigureDirective(Figure):
    """Extended directive for og-image as figure style.

    User pass content url as arguments instead of image url.
    In extension process, it converts from content to image.
    """

    option_spec = Figure.option_spec.copy()
    del option_spec["target"]

    def run(self):  # noqa: D102
        self.options["target"] = self.arguments[0]
        nodeset = super().run()
        imageref = nodeset[0].children[-1]
        image = imageref[0] if imageref.children else imageref
        # Flag that image uri is set content URL, and fetch metadata by OgpDomain.
        image["mark-ogpy"] = True
        return nodeset


class OGPDomain(Domain):
    """Domain to manage contents metadata.

    This has client and cache store.
    """

    name = "ogp"
    label = "OGPy Image manageent"
    directives = {
        "image": OGPImageDirective,
        "figure": OGPFigureDirective,
    }

    @property
    def caches(self) -> dict[str, Tuple[types.Metadata | types.MetadataFuzzy, int]]:
        """Cache storage for OGP metadata."""
        self.data.setdefault("caches", {})
        return self.data["caches"]

    @property
    def use_browser(self) -> bool:
        return self.env.config.ogp_use_browser

    @property
    def browser_name(self) -> str:
        return self.env.config.ogp_browser_name

    def _fetch_for_cache(
        self, url
    ) -> Tuple[types.Metadata | types.MetadataFuzzy, int | None]:
        if self.use_browser:
            from ogpy.client import browser

            return browser.fetch_for_cache(url, browser_name=self.browser_name)  # type: ignore[arg-type]
        return fetch_for_cache(url)

    def _get_metadata(self, url) -> types.Metadata | types.MetadataFuzzy:
        """Retrieve metadata of url.

        When data is cached and reusable, use cache.
        """
        now = datetime.now()
        if url in self.caches:
            data, cache_expired = self.caches[url]
            if cache_expired >= int(now.timestamp()):
                return data

        data, expired = self._fetch_for_cache(url)
        if expired:
            self.caches[url] = (data, expired)
        return data

    def process_doc(
        self, env: BuildEnvironment, docname: str, document: nodes.document
    ):
        """Find images flagged as ``mark-ogpy`` and replace uri by metadata."""
        for node in document.findall(nodes.image):
            if "mark-ogpy" not in node:
                continue
            data = self._get_metadata(node["uri"])
            if not data.images:
                logger.warning("Image property is not exists.")
                continue
            image_prop = data.images[0]
            node["uri"] = image_prop.url
            if "width" not in node and image_prop.width:
                node["width"] = f"{image_prop.width}px"
            if "height" not in node and image_prop.height:
                node["height"] = f"{image_prop.height}px"


def setup(app: Sphinx):
    """Entrypoint as Sphinx-extension."""
    app.add_domain(OGPDomain)
    app.add_config_value("ogp_use_browser", False, "env", bool)
    app.add_config_value("ogp_browser_name", "chromium", "env", str)
    return {
        "version": importlib.metadata.version("ogpy"),
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
