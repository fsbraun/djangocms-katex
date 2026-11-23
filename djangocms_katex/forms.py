# forms.py
#

import json

from django import forms
from django.conf import settings
from django.forms import ModelForm

from . import conf, models


class KaTexInput(forms.Textarea):
    class Media:
        js = (
            "djangocms_katex/admin/js/preview.js",
            "djangocms_katex/vendor/katex/katex.min.js",
            "djangocms_katex/vendor/katex/contrib/mhchem.min.js",
            "admin/vendor/ace/ace.js"
            if "djangocms_static_ace" in settings.INSTALLED_APPS
            else "https://cdnjs.cloudflare.com/ajax/libs/ace/1.45.2/ace.js",
        )
        css = {"all": ("djangocms_katex/admin/css/preview.css", "djangocms_katex/vendor/katex/katex.css")}

    def __init__(self, *args, **kwargs):
        self.textarea_template = self.template_name
        self.template_name = "djangocms_katex/admin/katex_widget.html"
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["textarea_template"] = self.textarea_template
        # Site-wide options and macros, so that the preview matches the rendered page
        context["widget"]["katex_config"] = json.dumps(
            {"options": conf.get_katex_options(), "macros": conf.get_katex_macros()}
        )
        return context


class KaTexForm(ModelForm):
    class Meta:
        model = models.KaTex
        widgets = {
            "katex": KaTexInput,
        }
        fields = "__all__"
