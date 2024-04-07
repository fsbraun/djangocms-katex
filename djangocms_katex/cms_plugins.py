# djangocms_katex/cms_plugins.py
#

import json
import re

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
    text_icon = ('<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                 'x="0px" y="0px" viewBox="0 0 121.83 122.88">'
                 '<g><path d="M27.61,34.37l-4.07,4.6l0.4,1.74h10.48c-2.14,12.38-3.74,23.54-6.81,40.74c-3.67,21.94-5.78,27.33-7.03,29.3 c-1.1,1.95-2.68,2.96-4.82,2.96c-2.35,0-6.6-1.86-8.88-3.97c-0.82-0.56-1.79-0.42-2.82,0.26C2,111.74,0,114.42,0,116.82 c-0.12,3.24,4.21,6.06,8.34,6.06c3.64,0,9-2.28,14.64-7.64c7.71-7.31,13.48-17.34,18.3-39.02c3.1-13.84,4.56-22.84,6.74-35.5 l13.02-1.18l2.82-5.17H49.2C52.99,10.53,55.95,7,59.59,7c2.42,0,5.24,1.86,8.48,5.52c0.96,1.32,2.4,1.18,3.5,0.28 c1.85-1.1,4.13-3.92,4.28-6.48C75.96,3.5,72.6,0,66.82,0C61.58,0,53.55,3.5,46.8,10.38c-5.92,6.27-9.02,14.1-11.16,23.99H27.61 L27.61,34.37z M69.27,50.33c4.04-5.38,6.46-7.17,7.71-7.17c1.29,0,2.32,1.27,4.53,8.41l3.78,12.19 c-7.31,11.18-12.66,17.41-15.91,17.41c-1.08,0-2.17-0.34-2.94-1.1c-0.76-0.76-1.6-1.39-2.42-1.39c-2.68,0-6,3.25-6.06,7.28 c-0.06,4.11,2.82,7.05,6.6,7.05c6.49,0,11.98-6.37,22.58-23.26l3.1,10.45c2.66,8.98,5.78,12.81,9.68,12.81 c4.82,0,11.3-4.11,18.37-15.22l-2.96-3.38c-4.25,5.12-7.07,7.52-8.74,7.52c-1.86,0-3.49-2.84-5.64-9.82l-4.53-14.73 c2.68-3.95,5.32-7.27,7.64-9.92c2.76-3.15,4.89-4.49,6.34-4.49c1.22,0,2.28,0.52,2.94,1.25c0.87,0.96,1.39,1.41,2.42,1.41 c2.33,0,5.93-2.96,6.06-6.88c0.12-3.64-2.14-6.74-6.06-6.74c-5.92,0-11.14,5.1-21.19,20.04l-2.07-6.41 c-2.9-9-4.82-13.63-8.86-13.63c-4.7,0-11.16,5.78-17.48,14.94L69.27,50.33L69.27,50.33z"/>'
                 '</g></svg>')

    def render(self, context, instance, placeholder):
        context["options"] = json.dumps({
            "throwOnError": False,
            "displayMode": instance.katex_display_style >= 1,
            "fleqn": instance.katex_display_style == 2,
        })
        context["tag_type"] = "div" if instance.katex_display_style else "span"
        context["chem_eq"] = re.search(r"\\ce\s*{", instance.katex)
        return super().render(context, instance, placeholder)
