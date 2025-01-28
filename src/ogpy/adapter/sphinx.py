"""OGPy Sphinx adapter."""

import importlib.metadata

from docutils import nodes
from docutils.parsers.rst import directives
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
            image_prop = data.images[0]
            ref = nodes.reference(refuri=data.url)
            image = nodes.image(uri=image_prop.url, alt=image_prop.alt or data.title)
            if image_prop.width:
                image["width"] = f"{image_prop.width}px"
            if image_prop.height:
                image["height"] = f"{image_prop.height}px"
            ref.append(image)
            figure = nodes.figure("", ref)
            if "align" in node:
                figure["align"] = node["align"]
            node.append(figure)


class OGPImageLinkDirective(SphinxDirective):
    has_content = False
    required_arguments = 1
    option_spec = {
        "align": directives.unchanged,
    }

    def run(self):  # noqa: D102
        node = ogp_image_link()
        node.attributes = self.options
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
