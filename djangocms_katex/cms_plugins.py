import json

from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.cms_plugins import CMSUIPlugin
from djangocms_frontend.common.attributes import AttributesMixin
from djangocms_frontend.common.responsive import ResponsiveMixin
from djangocms_frontend.common.spacing import SpacingMixin
import djangocms_katex
from . import forms, models

mixin_factory = settings.get_renderer(djangocms_katex)


@plugin_pool.register_plugin
class KaTexPlugin(
    mixin_factory("KaTex"), AttributesMixin, ResponsiveMixin, SpacingMixin, CMSUIPlugin
):
    """
    """

    name = _("KaTeX Formula")
    module = _("Frontend")
    model = models.KaTex
    form = forms.KaTexForm
    render_template = "djangocms_katex/formula.html"
    change_form_template = "djangocms_katex/admin/katex.html"
    text_enabled = True

    fieldsets = [
        (
            None,
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
            "displayMode": instance.katex_display_style == "True",
        })
        context["tag_type"] = "div" if instance.katex_display_style == "True" else "span"
        return super().render(context, instance, placeholder)
