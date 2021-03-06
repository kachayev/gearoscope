import os, sys

# Working directory (current file one)
WORKDIR = os.path.dirname(__file__)

# This will give us oppurtunities to keep applications in separated directory
# and prevent chaus in main project directory
sys.path.append(os.path.join(WORKDIR, 'apps'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alexey Kachayev', 'kachayev@gmail.com'),
    ('Iurii Ogienko', 'iurii.ogiienko@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(WORKDIR, 'scoper.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(WORKDIR, 'static', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = '/static/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
COMMON_STATIC_ROOT = os.path.join(WORKDIR, 'static')
STATIC_ROOT = ''

# URL prefix for static files.
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (COMMON_STATIC_ROOT,)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rl5*7@(s^7b!hc&t-&970e9zq37f9@cqcnd#kd42&fd_2gi2x8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'gearoscope.urls'

TEMPLATE_DIRS = (
    os.path.join(WORKDIR, 'templates')
)

INSTALLED_APPS = (
    # django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # 3rd party apps
    'gunicorn',

    # project relative apps
    'dashboard',
    'scoper',
    'monitor',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Path to sonar daemon logger file
# Don't fogget, that runningW sonar daemon
# should have permissions to read/write this file
SONAR_LOG_FILE = os.path.join(WORKDIR, 'data', 'sonar.log')

# Path to sonar daemon configuration file
# Don't fogget, that running sonar daemon
# should have permissions to read/write this file
SONAR_CONFIGURATION_FILE = os.path.join(WORKDIR, 'data', 'sonar.conf')

# Count of pings per each action of pingator agents
# More retries will help you to calculate average response time
# less rought, but it will take more time and generate more
# trafic in network channel. 4 retries is a common way to do pings.
SONAR_PINGATOR_RETRIES = 4

# Dict with all information for creating Sonar agent pools.
# Each of this pool will consist from <count> number of
# threads with sync Queue object, which can be used for
# pushing tasks to pool (to be executed by thread agents)
SONAR_AGENT_POOLS = {
    'stat': {
        'timeout': 0,
        'count': 3,
        'prototype': 'sonar.agents.process.ProcessStatAgent'
    }
}

# Maximum records to read from sonar log file per each
# log analizer action. Do not use too much lines to prevent
# problems with memory and CPU leaks
DASHBOARD_LOG_LIMIT = 1000

