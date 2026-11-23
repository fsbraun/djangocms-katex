# djangocms_katex/conf.py
#

from django.conf import settings


def get_katex_options():
    """Site-wide KaTeX options (see https://katex.org/docs/options). Must be JSON-serializable."""
    return dict(getattr(settings, "DJANGOCMS_KATEX_OPTIONS", {}))


def get_katex_macros():
    """Site-wide KaTeX macros, e.g. ``{"\\RR": "\\mathbb{R}"}``, available in all formulae."""
    return dict(getattr(settings, "DJANGOCMS_KATEX_MACROS", {}))
