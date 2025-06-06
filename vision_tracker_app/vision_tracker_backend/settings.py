"""
Django settings for vision_tracker_backend project.

Generated by 'django-admin startproject' using Django 5.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

# vision_tracker_app/vision_tracker_app/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv # NEW: Import load_dotenv
import firebase_admin # Keep this here for firebase_admin._apps check later
from firebase_admin import credentials, firestore # Keep this here

# 1. Load environment variables FIRST
load_dotenv() # This loads the variables from .env into os.environ

# 2. Define BASE_DIR (Project Root)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+^_quh$u@)my_l^tps42kcye!9+fm#h@85yj5oap2vdkt(*5#j" # This can stay

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# 3. Access environment variables after dotenv is loaded
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Custom Application Settings
VISION_STATEMENT_FULL = (
    "I am a good leader, continuously refreshing my skills and expanding my network with inspiring individuals. "
    "Grounded in spiritual and emotional maturity, I make wise decisions, foster dignity, and communicate with articulate grace. "
    "As a devoted husband and father, a creative problem-solver, and a champion for accessible innovation, "
    "I leave a profound and positive mark on every life I touch and every challenge I undertake."
)



# 4. Firebase Initialization - NOW AFTER BASE_DIR IS DEFINED
print(f"DEBUG: Checking Firebase initialization...") # Debug print
if not firebase_admin._apps: # Checks if an app is already initialized
    FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'firebase_credentials.json')
    print(f"DEBUG: Looking for Firebase credentials at: {FIREBASE_CREDENTIALS_PATH}") # Debug print
    if os.path.exists(FIREBASE_CREDENTIALS_PATH):
        try:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully!") # SUCCESS print
        except Exception as e:
            print(f"ERROR: Error initializing Firebase Admin SDK: {e}") # ERROR print
    else:
        print("ERROR: Firebase credentials file not found. Firebase Admin SDK not initialized.") # FILE NOT FOUND print
else:
    print("DEBUG: Firebase Admin SDK already initialized.") # ALREADY INITIALIZED print


# Application definition (rest of your settings, no changes needed here)
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "vision_tracker_api",
    "corsheaders", # Make sure corsheaders is here too!
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = "vision_tracker_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "vision_tracker_backend.wsgi.application"

# In vision_tracker_app/settings.py
ASGI_APPLICATION = 'vision_tracker_backend.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173", 
]

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
