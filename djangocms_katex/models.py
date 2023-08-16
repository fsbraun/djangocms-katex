from django.utils.translation import gettext_lazy as _

from djangocms_frontend.models import FrontendUIItem


class KaTex(FrontendUIItem):

    class Meta:
        proxy = True
        verbose_name = _("KaTeX Formula")

    def get_short_description(self):
        return f"({self.katex})"
