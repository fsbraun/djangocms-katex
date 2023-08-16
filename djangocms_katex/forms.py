from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.common.responsive import ResponsiveFormMixin
from djangocms_frontend.common.spacing import SpacingFormMixin
from djangocms_frontend.contrib import alert
from djangocms_frontend.fields import (
    AttributesFormField,
    ColoredButtonGroup,
    TagTypeFormField,
)
from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.settings import COLOR_STYLE_CHOICES

mixin_factory = settings.get_forms(alert)


class KaTexForm(
    mixin_factory("KaTex"), ResponsiveFormMixin, SpacingFormMixin, EntangledModelForm
):

    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "katex",
                "katex_display_style",
                "attributes",
            ]
        }

    katex = forms.CharField(
        label=_("Formula"),
    )
    katex_display_style = forms.ChoiceField(
        label=_("Style"),
        initial=False,
        choices=((False, _("Inline style")), (True, ("Display style"))),
        required=False,
        help_text=_("Switch between inline and display style"),
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()
