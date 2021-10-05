import os
from pathlib import Path
from Config.Settings.Base import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

# CORS Headers
# CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    "http://0.0.0.0",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3010",
    "http://localhost:3011",
    "http://localhost:3021",
    "http://127.0.0.1"
]

CORS_ORIGIN_WHITELIST = (
    "http://0.0.0.0",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3010",
    "http://localhost:3011",
    "http://localhost:3021",
    "http://127.0.0.1"
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