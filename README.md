# rwswfm
# pip install -r requirements.txt
Django
gunicorn
psycopg[binary]
python-dotenv
django-extensions
django-template-partials
django-htmx
django-crispy-forms
crispy-bootstrap5

# cmd activate env -> goto folder existing git folder [\Projects\rwswfm] and startproject
django-admin startproject rwswfm .

# start a core app
python manage.py startapp core

# correct DB in settings.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# change to get secret key from .env file
SECRET_KEY = os.getenv('SECRET_KEY')

# change to get debug option from .env file
DEBUG = os.getenv('DEBUG')

# INSTALLED_APPS
    'django_extensions',
    'core',
    'django_htmx',
    'debug_toolbar', # need to pip install django-debug-toolbar
    'crispy_forms',
    'crispy_bootstrap5',
    'template_partials',

# MIDDLEWARE
	'debug_toolbar.middleware.DebugToolbarMiddleware',
	'django_htmx.middleware.HtmxMiddleware',
	
# DATABASES	
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PWD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS':  {
            'sslkey': {'ca': os.path.join(BASE_DIR, 'ca.pem')
            }
        }
    }
}

# STATICFILES_DIRS -> add this option when having static folder under project
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# CRISPY FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# change secret key in .env file & correct DB information

# create forms, views, models folder under core app. Remember to have __init__.py file in each folder
# from your_files.py import *
# remove forms.py, views.py under core/

# add urls.py under core app

# Using django.contrib.auth so:
# in settings.py need have
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login'

# Custom User model
AUTH_USER_MODEL = 'core.User'

# in rwswfm\urls.py, add below to urlspattern
path('', include('django.contrib.auth.urls')),

# add core\templates
# add registration\login.html
# add templates\base.html



# Models:
Carrier (sample):

User(AbstractUser)

Team:
- name
- active
- slug

Task:
- name
- active
- team
- slug

Vendor:
- name
- active
- slug

Employee
- empid
- name
- active
- vendor

Assignment
- employee
- task
- user_id
- dstamp
- mi_estimate
- mi_actual
- status

