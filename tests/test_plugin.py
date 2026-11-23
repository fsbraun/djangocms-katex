import json
import re
from html import unescape
from io import StringIO

import pytest
from cms.plugin_pool import plugin_pool
from django.contrib.staticfiles import finders
from django.core.management import call_command
from django.template import engines
from django.template.loader import render_to_string

from djangocms_katex.cms_plugins import KaTexPlugin
from djangocms_katex.forms import KaTexForm
from djangocms_katex.models import KaTex


def render_plugin(rf, formula, display_style=1):
    """Renders the plugin including its sekizai blocks, returns the page's html"""
    instance = KaTex(katex=formula, katex_display_style=display_style)
    context = KaTexPlugin().render({}, instance, None)
    return render_to_string("base.html", context, request=rf.get("/"))


def data_attribute(html, name):
    return json.loads(unescape(re.search(rf'{name}="([^"]*)"', html).group(1)))


def test_plugin_is_registered():
    assert plugin_pool.get_plugin("KaTexPlugin") is KaTexPlugin


@pytest.mark.parametrize(
    "display_style, tag, options",
    [
        (0, "span", {"displayMode": False, "fleqn": False}),
        (1, "div", {"displayMode": True, "fleqn": False}),
        (2, "div", {"displayMode": True, "fleqn": True}),
    ],
)
def test_display_styles(rf, display_style, tag, options):
    html = render_plugin(rf, "a^2 + b^2 = c^2", display_style)

    assert f'<{tag} data-katex-rendered="false"' in html
    assert f"a^2 + b^2 = c^2</{tag}>" in html
    assert data_attribute(html, "data-options") == options


def test_formula_source_is_escaped(rf):
    html = render_plugin(rf, 'a < b \\text{"<script>"}')

    assert "a &lt; b \\text{&quot;&lt;script&gt;&quot;}</div>" in html


def test_assets(rf):
    html = render_plugin(rf, "x")

    assert "djangocms_katex/vendor/katex/katex.min.css" in html
    assert "djangocms_katex/css/formula.css" in html
    assert "djangocms_katex/vendor/katex/katex.min.js" in html
    assert "djangocms_katex/js/render.js" in html
    # No inline scripts: Compatible with a strict content security policy
    assert not re.search(r"<script(?![^>]*\bsrc=)", html)
    for asset in re.findall(r'(?:src|href)="/static/([^"]+)"', html):
        assert finders.find(asset), f"{asset} is not a static file"


@pytest.mark.parametrize(
    "formula, expected",
    [("E = mc^2", False), ("\\ce{H2O}", True), ("\\ce {H2O}", True), ("\\pu{1 mol}", True), ("\\cdot", False)],
)
def test_mhchem_is_only_loaded_for_chemical_formulae(rf, formula, expected):
    html = render_plugin(rf, formula)

    assert ('<script defer src="/static/djangocms_katex/vendor/katex/contrib/mhchem.min.js">' in html) is expected


def test_config_defaults(rf):
    config = data_attribute(render_plugin(rf, "x"), "data-config")

    assert config == {
        "katex": "/static/djangocms_katex/vendor/katex/katex.min.js",
        "mhchem": "/static/djangocms_katex/vendor/katex/contrib/mhchem.min.js",
        "options": {},
        "macros": {},
    }


def test_config_from_settings(rf, settings):
    settings.DJANGOCMS_KATEX_OPTIONS = {"leqno": True, "strict": "ignore"}
    settings.DJANGOCMS_KATEX_MACROS = {"\\RR": "\\mathbb{R}"}

    config = data_attribute(render_plugin(rf, "x \\in \\RR"), "data-config")

    assert config["options"] == {"leqno": True, "strict": "ignore"}
    assert config["macros"] == {"\\RR": "\\mathbb{R}"}


def test_form_widget(settings):
    settings.DJANGOCMS_KATEX_MACROS = {"\\RR": "\\mathbb{R}"}

    form = KaTexForm()
    html = str(form["katex"])
    media = str(form.media)

    assert 'id="katex-ace-editor"' in html
    assert '<textarea name="katex"' in html
    assert data_attribute(html, "data-config") == {"options": {}, "macros": {"\\RR": "\\mathbb{R}"}}
    assert "djangocms_katex/vendor/katex/katex.min.js" in media
    assert "djangocms_katex/admin/js/preview.js" in media


def test_short_description():
    assert KaTex(katex="x^2").get_short_description() == "(x^2)"


@pytest.mark.django_db
def test_no_missing_migrations():
    out = StringIO()
    try:
        call_command("makemigrations", "djangocms_katex", check=True, dry_run=True, stdout=out)
    except SystemExit:
        pytest.fail(f"Missing migrations:\n{out.getvalue()}")


def test_katex_assets_template_tag(rf):
    template = engines["django"].from_string(
        "{% load sekizai_tags djangocms_katex_tags %}{% render_block 'css' %}{% katex_assets %}{% katex_assets %}"
        "{% render_block 'js' %}"
    )
    html = template.render({}, rf.get("/"))

    assert html.count("djangocms_katex/vendor/katex/katex.min.css") == 1
    assert html.count("djangocms_katex/css/formula.css") == 1
    assert html.count('src="/static/djangocms_katex/js/render.js"') == 1
    assert "mhchem" not in html.split("data-config")[0]
    # Identical to the plugin's assets
    plugin_html = re.sub(r"<div data-katex-rendered.*?</div>|</?(html|head|body)>", "", render_plugin(rf, "x"))
    assert html.split() == plugin_html.split()


def test_katex_assets_template_tag_without_sekizai():
    assert engines["django"].from_string("{% load djangocms_katex_tags %}{% katex_assets %}").render({}) == ""
