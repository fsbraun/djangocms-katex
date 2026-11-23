# tests/settings.py
#
# Minimal django CMS project to test djangocms-katex

from importlib.util import find_spec
from pathlib import Path

SECRET_KEY = "djangocms-katex-test"
DEBUG = True
USE_TZ = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "cms",
    "menus",
    "treebeard",
    "sekizai",
    "djangocms_katex",
]

if find_spec("djangocms_markdown"):
    # Optional: djangocms-katex adds formulae to djangocms-markdown
    INSTALLED_APPS.append("djangocms_markdown")

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path(__file__).parent / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
            ],
        },
    },
]

ROOT_URLCONF = "tests.urls"
STATIC_URL = "/static/"
SITE_ID = 1
LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English")]
CMS_TEMPLATES = [("base.html", "Base")]
CMS_CONFIRM_VERSION4 = True
