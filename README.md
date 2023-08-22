# djangocms-katex

[![PyPI version](https://badge.fury.io/py/djangocms-katex.svg)](https://badge.fury.io/py/djangocms-katex)
[![Python version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://pypi.org/project/djangocms-katex/)
[![Django version](https://img.shields.io/badge/django-3.2--4.2-blue.svg)](https://www.djangoproject.com/)
[![django CMS version](https://img.shields.io/badge/django%20CMS-3.8%2B-blue.svg)](https://www.django-cms.org/)
[![django CMS 4](https://img.shields.io/badge/django%20CMS-4-blue.svg)](https://www.django-cms.org/en/preview-django-cms-40/)

Provides a django CMS plugin to render formulae using KaTeX and 
its mhchem extension.

The plugin can display formulae either inline or in display mode. 
It is text-enabled, and you can add equations to rich text fields 
of djangocms-text-ckeditor.

The plugin form has a preview functionality that either shows
the typed formula. Errors are shown in red.

![Example screenshot](https://github.com/fsbraun/djangocms-katex/blob/main/private/screenshot.jpg?raw=true)

## Installation

For a manual install:

* run `pip install djangocms-katex`
* add the following entries to your ``INSTALLED_APPS``:
  ```
      "djangocms_katex",
  ```

* run `python manage.py migrate`

The Code plugin uses the ace code editor which is loaded from a CDN by default.
If you want the ace code editor to be served from static files, please use
`djangocms-katex[static-ace]` instead of `djangocms-katex` in your
requirements or with pip. Make the static files for the ace code editor available
to your project by adding `djangocms_static_ace` to your project's
``INSTALLED_APPS``.

djangocms-text-ckeditor's inline functionality might interfere with KaTeX's layout.
To ensure a great editing experience deactivate it if you use djangocms-katex by
removing `TEXT_INLINE_EDITING = True` from your `settings.py` file.

## Usage

Once installed, a new puling ("KaTeX formula") is available and can be entered 
into any placeholder or within a text plugin.


djangocms-katex only loads required LaTeX JavaScript libraries on demand only. 
This might lead to formulae initially only shown in source code. To see the rendered
formula in such a case, please reload the page which ensures that all required
JavaScript is loaded.
