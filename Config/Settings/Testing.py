import os
from pathlib import Path
from Config.Settings.Base import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ["0.0.0.0", "cos.omr"]

# CORS Headers
CORS_ALLOWED_ORIGINS = [
    'http://cos.omr',
    'http://st0001.cos.omr',
    'http://st0201.cos.omr',
    'http://st1010.cos.omr',
    'http://st1011.cos.omr',
]

CORS_ORIGIN_WHITELIST = (
    'http://cos.omr',
    'http://st0001.cos.omr',
    'http://st0201.cos.omr',
    'http://st1010.cos.omr',
    'http://st1011.cos.omr',
)

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_CREDENTIALS = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ["POSTGRESQL_ALPHA_ENGINE"],
        "NAME": os.environ["POSTGRESQL_ALPHA_DATABASE"],
        "USER": os.environ["POSTGRESQL_ALPHA_USER"],
        "PASSWORD": os.environ["POSTGRESQL_ALPHA_PASSWORD"],
        # IMPORTANT: Database host as docker-compose service!
        "HOST": os.environ["POSTGRESQL_ALPHA_HOST"],
        "PORT": os.environ["POSTGRESQL_ALPHA_PORT"],
    }
}