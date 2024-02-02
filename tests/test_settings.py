import os


SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "feedback",
    "tests",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "testdb",
    },
}

AUTH_USER_MODEL = 'auth.User'

ROOT_URLCONF = 'feedback.services.urls'
