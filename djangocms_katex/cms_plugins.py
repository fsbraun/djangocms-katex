import json

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from . import forms, models


@plugin_pool.register_plugin
class KaTexPlugin(CMSPluginBase):
    """
    """

    name = _("KaTeX Formula")
    model = models.KaTex
    form = forms.KaTexForm
    render_template = "djangocms_katex/formula.html"
    text_enabled = True

    fieldsets = [
        (
            name,
            {
                "fields": [
                    "katex",
                    "katex_display_style",
                ]
            },
        ),
    ]

    def render(self, context, instance, placeholder):
        instance.options = json.dumps({
            "throwOnError": False,
            "displayMode": instance.katex_display_style,
        })
        context["tag_type"] = "div" if instance.katex_display_style else "span"
        return super().render(context, instance, placeholder)
