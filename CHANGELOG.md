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
