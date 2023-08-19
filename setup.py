#!/usr/bin/env python
from setuptools import setup, find_packages
from djangocms_katex import __version__


with open('README.md') as fh:
    long_description = fh.read()


CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Framework :: Django :: 3.2',
    'Framework :: Django :: 4.0',
    'Framework :: Django :: 4.1',
    'Framework :: Django :: 4.2',
    "Framework :: Django CMS :: 3.8",
    "Framework :: Django CMS :: 3.9",
    "Framework :: Django CMS :: 3.10",
    "Framework :: Django CMS :: 3.11",
    "Framework :: Django CMS :: 4.0",
    "Framework :: Django CMS :: 4.1",
]

EXTRA_REQUIREMENTS = {
    "static-ace": [
        "djangocms-static-ace",
    ],
}

setup(
    name='djangocms-katex',
    version=__version__,
    description='Provides plugin to render formulae in django CMS',
    author='Fabian Braun',
    author_email='fsbraun@gmx.de',
    url='https://github.com/fsbraun/djangocms-katex',
    packages=find_packages(exclude=['testapp', 'docs']),
    install_requires=[
        "django-cms"
    ],
    extras_require=EXTRA_REQUIREMENTS,
    license='MIT',
    platforms=['OS Independent'],
    keywords=['KaTeX', 'django CMS'],
    classifiers=CLASSIFIERS,
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
)
