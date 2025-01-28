"""OGPy Sphinx adapter."""

import importlib.metadata

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective

from ..client import fetch


class ogp_image_link(nodes.General, nodes.Element):  # noqa: D101,E501
    pass


class OGPDomain(Domain):
    name = __name__
    label = "ogpy"

    def process_doc(
        self, env: BuildEnvironment, docname: str, document: nodes.document
    ):
        for node in document.findall(ogp_image_link):
            data = fetch(node["url"])
            ref = nodes.reference(refuri=data.url)
            image = nodes.image(uri=data.images[0].url, alt=data.title)
            ref.append(image)
            node.append(nodes.figure("", ref))


class OGPImageLinkDirective(SphinxDirective):
    has_content = False
    required_arguments = 1

    def run(self):  # noqa: D102
        node = ogp_image_link()
        node["url"] = self.arguments[0]
        return [
            node,
        ]


def pass_it(self, node):
    pass


def setup(app: Sphinx):
    """Entrypoint as Sphinx-extension."""
    app.add_node(ogp_image_link, html=(pass_it, pass_it))
    app.add_directive("ogp-image-link", OGPImageLinkDirective)
    app.add_domain(OGPDomain)
    return {
        "version": importlib.metadata.version("ogpy"),
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
