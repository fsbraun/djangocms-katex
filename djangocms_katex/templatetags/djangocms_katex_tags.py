from django import template

from .. import assets

register = template.Library()


@register.simple_tag(takes_context=True)
def katex_assets(context, chem=False):
    """Adds KaTeX's stylesheets and the script rendering all formulae of a page to the
    sekizai blocks ``css`` and ``js``. It outputs nothing::

        {% load djangocms_katex_tags %}
        {% katex_assets %}

    KaTeX itself is only loaded by the browser if the page contains formulae.
    """
    assets.add_assets(context, chem=bool(chem))
    return ""
