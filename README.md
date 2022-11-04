# Lazygram

Lazygram project is a copy of Instagram make with python Django and Reactjs, is a
simply, fast and functional social network to interconect with the world.

## Project status

This project are in development, comming soon in production.

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

## Development

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

For more information, see the following documentations.

- [Anymail(Mailgun)](https://anymail.dev/en/stable/esps/mailgun/)
- [Redis](https://redis.io/docs/getting-started/)
- [Django-redis](https://django-redis-cache.readthedocs.io/en/latest/)
- [Django-email](https://docs.djangoproject.com/en/4.1/ref/settings/#email-backend)
- [JWT](https://pyjwt.readthedocs.io/en/stable/)
- [Rest-framework](https://www.django-rest-framework.org/)
- [CORS](https://pypi.org/project/django-cors-headers/)
- [Rest-framework-simply-jwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html)

```Dockerfile
docker-compose -f local.yml build | docker-compose -f local.yml up
```

## How to use

It is very simply to use, you can do the following:

- Create your profile in Lazygram app.
- Upload your posts and follow your friends!
- Like, comment and save your favorite posts.
- Watch the premiere films in lazymovies and more!

## Version

BETA.

## License

[MIT License](https://choosealicense.com/licenses/mit/)
