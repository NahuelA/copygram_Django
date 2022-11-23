""" Cookies to users. """

# Settings
from config.settings import base

# Utils
from django.utils.cache import patch_vary_headers


def jwt_cookie(value, response):
    """Create simple and secure cookie."""

    if (value, response) is not None:
        # Set cookie
        response.set_cookie(
            key=base.SIMPLE_JWT["AUTH_COOKIE"],
            value=value,
            expires=base.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=base.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=base.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=base.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        # Set the Vary header since content varies with the sessiontoken cookie.
        patch_vary_headers(response, ("Cookie",))
    else:
        raise "Value: %s and response: %s need is not none."(value, response)

    return 0
