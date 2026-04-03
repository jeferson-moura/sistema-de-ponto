import dj_database_url
import os
from pathlib import Path
import os
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL')
    )
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # 👈 ESSA LINHA
]
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')