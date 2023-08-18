# djangocms-katex
Provides a django CMS plugin to render formulae using KaTeX.

The plugin can display formulae either inline or in display mode. 
It is text-enabled and you can add equations to rich text fields 
of djangocms-text-ckeditor.

The plugin form has a preview functionality that either shows
the typed formula. Errors are shown in red.


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

