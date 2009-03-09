# Django settings for payroll project.
import os.path
ROOT_PATH = '/Users/johnboxall/git/canadian_payroll/'

DEBUG = True

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'payroll'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.

SITE_ID = 1

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    "django.contrib.admin",
    'employee',
    'payroll',
)

MEDIA_ROOT = os.path.join(ROOT_PATH,'static/')
TEMPLATE_DIRS = [os.path.join(ROOT_PATH,'templates/')]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'canadian_payroll.urls'


