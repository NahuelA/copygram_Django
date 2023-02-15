# Lazygram

Lazygram project is a copy of Instagram make with python Django and Reactjs, is a
simply, fast and functional social network to interconect with the world.

## Project status

This project are in development, comming soon in production.

## How to use

It is very simply to use, you can do the following:

- Create your profile in Lazygram app.
- Upload your posts and follow your friends!
- Like, comment and save your favorite posts.
- Watch the premiere films in lazymovies and more!

## Build and up project in your local machine

To starting, this command will install the [dev dependencies](https://github.com/NahuelA/lazygram_Django/blob/development/requirements/local.txt) and will setup your lazygram environment.

But first you need create your environment variables into an .env file.

``` bash
# General
SECRET_KEY="Your secret key"
DJANGO_ADMIN_URL="Your admin page url"


# Local
DJANGO_DEBUG=False


# Prod
DJANGO_ALLOWED_HOSTS="lazygram.com"
CONN_MAX_AGE=60
REDIS_URL="redis://127.0.0.1:6379/0"


# Security
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
DJANGO_SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF=True


# Email
DJANGO_DEFAULT_FROM_EMAIL="example <noreply@example.com>"
DJANGO_SERVER_EMAIL="<noreply@example.com>"
DJANGO_EMAIL_SUBJECT_PREFIX="[example]"


# Anymail (Mailgun)
MAILGUN_API_KEY="Your api key"
MAILGUN_DOMAIN="<noreply@example.com>"
```

**Build and up containers:**

``` bash
docker-compose -f local.yml build | docker-compose -f local.yml up
```

## Dependencies

### Base dependencies

``` bash
# Base
pytz==2022.1
python-slugify==6.1.0
Pillow==9.2.0
psycopg2==2.9.3 --no-binary psycopg2

# Django
django==4.0.2

# Cors for use react
django-cors-headers==3.12.0

# DjangoRESTFramework
djangorestframework==3.13.0

# Environment
django-environ==0.8.1

# Json Web Token
PyJWT>=2.4.0
djangorestframework-simplejwt

# Passwords security
argon2-cffi==21.2.0

# Static files
whitenoise==6.1.0

# Celery
redis>=3.0.0,<=4.0.0
django-redis==5.1.0
celery==5.2.7
flower==1.0.0
```

### Local dependencies

``` bash
-r ./base.txt

# Debugging
ipdb==0.13.7

# Testing
mypy==0.971
pytest==7.1.0
pytest-sugar==0.9.4
pytest-django==4.5.1
factory-boy==3.2.0

# Code quality
flake8==4.0.0
```

### Production dependencies

``` bash
# PRECAUTION: avoid production dependencies that aren't in development

-r ./base.txt

gunicorn==20.0.4

# Email
django-anymail[mailgun]==8.5
```

For more information, visit the following documentation:

- [Django-email](https://docs.djangoproject.com/en/4.1/ref/settings/#email-backend)
- [JWT](https://pyjwt.readthedocs.io/en/stable/)
- [Rest-framework](https://www.django-rest-framework.org/)
- [CORS](https://pypi.org/project/django-cors-headers/)
- [Rest-framework-simply-jwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html)
- [Redis](https://redis.io/docs/getting-started/) v4.0.0
- [Django-redis](https://django-redis-cache.readthedocs.io/en/latest/) v5.1.0
- [Anymail(Mailgun)](https://anymail.dev/en/stable/esps/mailgun/) v8.5

## Features

### Users

- [x] Sign up/in
  - In this app
  - With your google account
- [x] Session and Token authtentication
- [x] Follow your favorites accounts.

### Posts

- [x] Like
- [x] Comment
- [x] Save

## Features to implement

- [] Dark-mode
- [] Direct messages
- [] Stories
- [] Reels
- [] Share posts

_For more information, read the following:_
[Features in production | development](https://github.com/NahuelA/lazygram_Django/blob/development/development.rst)

## Version

BETA.

## License

[MIT License](https://choosealicense.com/licenses/mit/)
