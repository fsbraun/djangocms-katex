from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangocms_attributes_field.fields import AttributesField


class KaTex(CMSPlugin):

    class Meta:
        verbose_name = _("KaTeX Formula")

    katex = models.TextField(
        verbose_name=_("Formula"),
        blank=False,
    )
    katex_display_style = models.BooleanField(
        verbose_name=_("Style"),
        choices=((False, _("Inline style")), (True, _("Display style"))),
        help_text=_("Switch between inline and display style"),
    )
    attributes = AttributesField()

    def get_short_description(self):
        return f"({self.katex})"
