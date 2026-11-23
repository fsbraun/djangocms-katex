# djangocms_katex/assets.py
#
# Stylesheets and scripts needed to render formulae on a page. Used by the plugin, the
# ``katex_assets`` template tag and the djangocms-markdown integration, so that all of
# them add identical snippets to the sekizai blocks (sekizai then loads each only once).

import json
import re

from django.templatetags.static import static
from django.utils.html import format_html

from . import conf

CHEM_RE = re.compile(r"\\(ce|pu)\s*{")  # Formulae requiring KaTeX's mhchem extension

KATEX_CSS = "djangocms_katex/vendor/katex/katex.min.css"
KATEX_JS = "djangocms_katex/vendor/katex/katex.min.js"
MHCHEM_JS = "djangocms_katex/vendor/katex/contrib/mhchem.min.js"
FORMULA_CSS = "djangocms_katex/css/formula.css"
RENDER_JS = "djangocms_katex/js/render.js"


def get_render_config():
    """Page-wide configuration, read by render.js from its script tag"""
    return {
        "katex": static(KATEX_JS),
        "mhchem": static(MHCHEM_JS),
        "options": conf.get_katex_options(),
        "macros": conf.get_katex_macros(),
    }


def get_assets(chem=False):
    """Returns the html snippets for the sekizai blocks ``css`` and ``js``. mhchem is only
    included if ``chem`` is true; render.js loads it on demand otherwise."""
    js = [format_html('<script defer src="{}"></script>', static(KATEX_JS))]
    if chem:
        js.append(format_html('<script defer src="{}"></script>', static(MHCHEM_JS)))
    js.append(
        format_html(
            '<script defer src="{}" data-djangocms-katex data-config="{}"></script>',
            static(RENDER_JS),
            json.dumps(get_render_config()),
        )
    )
    return {
        "css": [
            format_html('<link rel="stylesheet" href="{}">', static(KATEX_CSS)),
            format_html('<link rel="stylesheet" href="{}">', static(FORMULA_CSS)),
        ],
        "js": js,
    }


def add_assets(context, chem=False):
    """Adds the assets to the sekizai blocks of the template context, as sekizai's
    ``{% addtoblock %}`` does. Does nothing if sekizai's context processor is not enabled."""
    from sekizai.helpers import get_varname

    data = context.get(get_varname())
    if data is None:
        return
    for block, snippets in get_assets(chem=chem).items():
        for snippet in snippets:
            data[block].append(snippet)
