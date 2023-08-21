# djangocms_katex/models.py
#

from cms.models import CMSPlugin
from django.db import models
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class KaTex(CMSPlugin):

    DISPLAY_STYLES = (
        (0, _("Inline style")),
        (1, _("Display style")),
        (2, _("Display style flush left")),
    )
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
    katex_display_style = models.SmallIntegerField(
        verbose_name=_("Style"),
        choices=DISPLAY_STYLES,
        null=False,
        default=1,
        help_text=_("Switch between styles"),
    )

    def get_short_description(self):
        """Provides a short description shown in the structure board. This will show the
        formula's source text."""
        return f"({self.katex})"
