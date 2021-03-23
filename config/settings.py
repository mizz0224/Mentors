"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "igvw9!mc_*oh&3(4*($6xf6sshil5&oqz8#7s!d268tkuoy8^%"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = ["django_countries", "django_seed"]

PROJECT_APPS = [
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "conversations.apps.ConversationsConfig",
    "posts.apps.PostsConfig",
    "reservations.apps.ReservationsConfig",
    "reviews.apps.ReviewsConfig",
    "wishlists.apps.WishlistsConfig",
]
SOCIAL_LOGIN_APPS = [
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.naver",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.github",
]


INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS + SOCIAL_LOGIN_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                # `allauth` needs this from django
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_URL = "/static/"

AUTH_USER_MODEL = "users.User"

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

MEDIA_URL = "/media/"


# Email ConfigurationINTERNAL_IPS
EMAIL_HOST = "smtp.mailgun.org"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("MAILGUN_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("MAILGUN_PASSWORD")
EMAIL_FROM = "mentors@sandboxee6ba1decc8d4a8fbae7c30bbaf7eed9.mailgun.org"


# django-allauth 부분
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    # 'allauth'와 관계없이 Django 관리자에서 사용자 이름으로 로그인 해야함.
    "django.contrib.auth.backends.ModelBackend",
    # e-mail로 로그인 하는 것과 같은 'allauth' 특정 인증 방법
    "allauth.account.auth_backends.AuthenticationBackend",
)
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "facebook": {
        "METHOD": "oauth2",
        "SDK_URL": "//connect.facebook.net/{locale}/sdk.js",
        "SCOPE": ["email", "public_profile"],
        "AUTH_PARAMS": {"auth_type": "reauthenticate"},
        "INIT_PARAMS": {"cookie": True},
        "FIELDS": [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "name",
            "name_format",
            "picture",
            "short_name",
            "email",
        ],
        "EXCHANGE_TOKEN": True,
        "LOCALE_FUNC": "path.to.callable",
        "VERIFIED_EMAIL": False,
        "VERSION": "v7.0",
    },
    "github": {
        "SCOPE": [
            "user",
            "repo",
            "read:org",
        ],
    },
    "kakao": {
        "APP": {
            "client_id": os.environ.get("KAKAO_API_KEY"),
            "secret": os.environ.get("KAKAO_ID"),
            "key": "",
        }
    },
}
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
LOGIN_REDIRECT_URL = "/"  # django-allauth 인증후 돌아갈 url
SOCIALACCOUNT_AUTO_SIGNUP = False  # django-allauth 인증후 계정없을시 자동생성여부
ACCOUNT_FORMS = {
    "signup": "users.forms.SocialSignUpForm"
}  # django-allauth 회원가입 form 설정, forms.py에서 SignupForm<-이거 상속안해주면 이중가입쳐리되므로 주의(대소문자구분)
SOCIALACCOUNT_FORMS = {"signup": "users.forms.SocialSignUpForm"}  # 상동
ACCOUNT_AUTHENTICATION_METHOD = "email"  # 계정 인증 방식(아마 로그인 방식인듯?)
ACCOUNT_EMAIL_REQUIRED = True  # 계정에 email이 필수form이여야하는가? default = false
ACCOUNT_UNIQUE_EMAIL = True  # unique email 즉 중복 이메일
ACCOUNT_USERNAME_REQUIRED = (
    False  # username 필요여부인데, 우리는 username 대신 name을 받아서 false로 지정
)
ACCOUNT_EMAIL_VERIFICATION = (
    None  # django-allauth에서 제공하는 email 인증방식인듯? django-allauth 가 아닐수도 있을것같은데 이부분은 공부 필요
)
