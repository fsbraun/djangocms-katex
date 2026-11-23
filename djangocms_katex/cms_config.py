# djangocms_katex/cms_config.py
#
# django CMS app registration (django CMS 4.1+): Adds formulae ($...$ and $$...$$) to
# djangocms-markdown, if it is installed. See djangocms_katex/markdown.py.

import json

from cms.app_base import CMSAppConfig
from django import forms
from django.templatetags.static import static
from django.utils.html import format_html

from . import assets, conf


class PreviewScript:
    """Script tag of the editor preview carrying the site-wide KaTeX options and macros"""

    path = "djangocms_katex/markdown/preview.js"

    def __html__(self):
        return format_html(
            '<script src="{}" data-djangocms-katex-preview data-config="{}"></script>',
            static(self.path),
            json.dumps({"options": conf.get_katex_options(), "macros": conf.get_katex_macros()}),
        )

    def __str__(self):
        return self.path

    def __eq__(self, other):
        return isinstance(other, PreviewScript)

    def __hash__(self):
        return hash(self.path)


def markdown_assets(html):
    """Page assets for rendered markdown: Only needed if it contains formulae"""
    if "data-katex-rendered" not in html:
        return None
    return assets.get_assets(chem=bool(assets.CHEM_RE.search(html)))


def markdown_editor_media():
    """KaTeX and the preview processor for djangocms-markdown's editor"""
    return forms.Media(
        css={"all": [assets.KATEX_CSS, assets.FORMULA_CSS]},
        js=[assets.KATEX_JS, assets.MHCHEM_JS, PreviewScript()],
    )


class KaTexCMSConfig(CMSAppConfig):
    djangocms_markdown_enabled = conf.markdown_enabled()
    djangocms_markdown_extensions = ["djangocms_katex.markdown"]
    djangocms_markdown_assets = markdown_assets
    djangocms_markdown_editor_media = markdown_editor_media
