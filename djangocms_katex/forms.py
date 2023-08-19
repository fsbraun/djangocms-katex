# forms.py
#

from django import forms
from django.conf import settings
from django.forms import ModelForm

from . import models


class KaTexInput(forms.Textarea):
    def __init__(self, *args, **kwargs):
        self.textarea_template = self.template_name
        self.template_name = "djangocms_katex/admin/katex_widget.html"
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["textarea_template"] = self.textarea_template
        return context



class KaTexForm(ModelForm):
    class Media:
        js = (
            "djangocms_katex/admin/js/preview.js",
            "djangocms_katex/vendor/katex/katex.min.js",
            "djangocms_katex/vendor/katex/contrib/mhchem.min.js",
            "admin/vendor/ace/ace.js"
            if "djangocms_static_ace" in settings.INSTALLED_APPS
            else "https://cdnjs.cloudflare.com/ajax/libs/ace/1.9.6/ace.js",

        )
        css = {"all": ("djangocms_katex/admin/css/preview.css", "djangocms_katex/vendor/katex/katex.css")}

    class Meta:
        model = models.KaTex
        widgets = {
            "katex": KaTexInput,
        }
        fields = "__all__"
