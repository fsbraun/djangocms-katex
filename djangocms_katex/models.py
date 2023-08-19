# djangocms_katex/models.py
#

from cms.models import CMSPlugin
from django.db import models
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class KaTex(CMSPlugin):

    class Meta:
        verbose_name = _("KaTeX Formula")

    katex = models.TextField(
        verbose_name=_("Formula"),
        blank=False,
        help_text=lazy(mark_safe, str)(
            _('Read more about KaTeX formulae in <a href="{link}" target="_blank">its documentation</a>')
            .format(link="https://katex.org")
        )  # A lazy string which will be marked safe
    )
    katex_display_style = models.BooleanField(
        verbose_name=_("Style"),
        choices=((False, _("Inline style")), (True, _("Display style"))),
        null=False,
        default=True,
        help_text=_("Switch between inline and display style"),
    )

    def get_short_description(self):
        """Provides a short description shown in the structure board. This will show the
        formula's source text."""
        return f"({self.katex})"
