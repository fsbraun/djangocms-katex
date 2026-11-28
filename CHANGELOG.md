Unreleased
==========

* feat: Display formulae in Markdown can also be enclosed in `\[` and `\]`, in addition
  to `$$`

1.1.0 (2026-11-23)
==================

* feat: Update KaTeX to 0.19.1. Note: Since KaTeX 0.18 its internal css classes are
  prefixed (e.g., `katex-base` instead of `base`). If your project styles KaTeX's
  internal classes, update your selectors.
* feat: Site-wide KaTeX options and macros with the new `DJANGOCMS_KATEX_OPTIONS` and
  `DJANGOCMS_KATEX_MACROS` settings. They also apply to the preview in the plugin form.
* feat: Formulae in Markdown: With djangocms-markdown 1.1+ write `$...$` and `$$...$$`
  in Markdown content, including a rendered editor preview. Can be switched off with
  `DJANGOCMS_KATEX_MARKDOWN = False`.
* feat: `{% katex_assets %}` template tag to add KaTeX's assets to a page
* feat: Formulae do not flash their LaTeX source before being rendered anymore
* feat: Wide formulae in display style scroll horizontally instead of overflowing the page
* feat: `\pu{}` loads the mhchem extension, too
* fix: Formulae added in edit mode render without a page reload: KaTeX and mhchem are
  loaded on demand
* fix: No inline scripts anymore: Compatible with a strict content security policy
* chore: Ace editor loaded from CDN updated to 1.45.2
* chore: Added tests for Django 4.2 - 6.1 and django CMS 3.11 - 5.1
* chore: Dropped support for Python 3.9

1.0.2 (2026-03-20)
==================

* chore: Update katex to 0.16.40

1.0.1 (2026-01-25)
==================

* chore: Update katex to 0.16.28

1.0.0 (2025-08-12)
==================

* Release 1.0: Stable now!!

0.5.3 (2024-04-07)
==================

* fix: Improved widget markup to better work with newer Django admin

0.5.2 (2023-10-02)
==================

* feat: Bundle KaTeX 0.16.9

0.5.0 (2023-08-22)
==================
* Add fleqn display style
* Add mdchem support

Note
=====
Version 0.5.0 is incompatible with previous versions. Delete djangocms-katex's
table and remove its entries from `django_migrations`, and run
`python ./manage.py migrate` again if you have installed an older
version.
