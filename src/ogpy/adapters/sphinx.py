"""OGPy Sphinx adapter."""

import importlib.metadata

from docutils import nodes
from docutils.parsers.rst.directives.images import Image
from sphinx.application import Sphinx
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment
from sphinx.util.logging import getLogger

from ..client import fetch

logger = getLogger(__name__)


class OGPDomain(Domain):
    name = __name__
    label = "ogpy"

    def process_doc(
        self, env: BuildEnvironment, docname: str, document: nodes.document
    ):
        for node in document.findall(nodes.image):
            if "mark-ogpy" not in node:
                continue
            data = fetch(node["uri"])
            if not data.images:
                logger.warning("Image property is not exists.")
                continue
            image_prop = data.images[0]
            node["uri"] = image_prop.url
            if "width" not in node and image_prop.width:
                node["width"] = f"{image_prop.width}px"
            if "height" not in node and image_prop.height:
                node["height"] = f"{image_prop.height}px"


class OGPImageLinkDirective(Image):
    option_spec = Image.option_spec.copy()
    del option_spec["target"]

    def run(self):  # noqa: D102
        self.options["target"] = self.arguments[0]
        nodeset = super().run()
        imageref = nodeset[-1]
        image = imageref[0] if imageref.children else imageref
        image["mark-ogpy"] = True
        return nodeset


def setup(app: Sphinx):
    """Entrypoint as Sphinx-extension."""
    app.add_directive("ogp-image-link", OGPImageLinkDirective)
    app.add_domain(OGPDomain)
    return {
        "version": importlib.metadata.version("ogpy"),
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
