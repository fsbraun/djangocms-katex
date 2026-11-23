# Integration with djangocms-markdown's extension hooks (djangocms-markdown 1.1+, django CMS 4.1+)

import json
import re
from html import unescape

import pytest
from django.template import engines

registry = pytest.importorskip("djangocms_markdown.registry")
pytest.importorskip("cms.app_registration")  # django CMS 3.11 does not load cms_config.py

from djangocms_markdown import rendering  # noqa: E402
from djangocms_markdown.widgets import MarkdownEditorWidget  # noqa: E402

from djangocms_katex import assets  # noqa: E402

TEXT = "Let $a_1 < b_1$ be:\n\n$$\n\\frac{a_1}{b_1} < 1\n$$\n\nAnd `$code$`."


def test_extension_is_registered():
    contribution = next(c for c in registry.get_contributions() if c.app == "djangocms_katex")

    assert contribution.extensions == ["djangocms_katex.markdown"]
    assert "djangocms_katex.markdown" in rendering.get_extensions()


def test_formulae_survive_rendering_and_sanitizing():
    html = rendering.render_markdown(TEXT)

    assert (
        '<span data-katex-rendered="false" data-options="{&quot;displayMode&quot;: false}">a_1 &lt; b_1</span>' in html
    )
    assert (
        '<div data-katex-rendered="false" data-options="{&quot;displayMode&quot;: true}">\\frac{a_1}{b_1} &lt; 1</div>'
        in html
    )
    assert "<code>$code$</code>" in html


def test_page_assets_are_those_of_the_plugin():
    html = rendering.render_markdown(TEXT)

    # Identical snippets: sekizai loads them once if a page has formula and markdown plugins
    assert rendering.get_assets(html) == assets.get_assets(chem=False)
    assert rendering.get_assets(rendering.render_markdown("$\\ce{H2O}$")) == assets.get_assets(chem=True)


def test_no_page_assets_without_formulae():
    assert rendering.get_assets(rendering.render_markdown("No formula for $5 to $10")) == {}


def test_markdown_assets_template_tag(rf):
    template = engines["django"].from_string(
        "{% load sekizai_tags djangocms_markdown_tags %}{% render_block 'css' %}"
        "{% with html=text|render_markdown %}{{ html }}{% markdown_assets html %}{% endwith %}"
        "{% render_block 'js' %}"
    )
    html = template.render({"text": TEXT}, rf.get("/"))

    assert html.count("djangocms_katex/vendor/katex/katex.min.css") == 1
    assert html.count('src="/static/djangocms_katex/js/render.js"') == 1
    assert html.index("katex.min.css") < html.index("data-katex-rendered") < html.index("render.js")


def test_editor_media(settings):
    settings.DJANGOCMS_KATEX_MACROS = {"\\RR": "\\mathbb{R}"}

    media = str(MarkdownEditorWidget().media)

    config = json.loads(
        unescape(re.search(r'preview\.js" data-djangocms-katex-preview data-config="([^"]*)"', media)[1])
    )
    assert config == {"options": {}, "macros": {"\\RR": "\\mathbb{R}"}}
    assert "djangocms_katex/vendor/katex/katex.min.css" in media
    # The preview script requires EasyMDE's editor script and KaTeX
    assert (
        media.index("djangocms_markdown/js/markdown_editor.js")
        < media.index("djangocms_katex/vendor/katex/katex.min.js")
        < media.index("djangocms_katex/vendor/katex/contrib/mhchem.min.js")
        < media.index("djangocms_katex/markdown/preview.js")
    )
