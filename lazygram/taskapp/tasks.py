"""Celery tasks."""

# Django
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

# Rest-framework
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Celery
from .celery import app


def verification_access_token(user):
    """Verify access token to change password."""
    access = AccessToken.for_user(user)
    tokens = {
        "access": str(access),
        "username": user.username,
    }

    return tokens


def verification_refresh_token(user):
    """Verify account with JWT."""

    refresh = RefreshToken.for_user(user)

    tokens = {
        "refresh": str(refresh),
        "username": user.username,
    }

    return tokens


@app.task(name="send_confirmation_email", max_retries=3)
def send_confirmation_email(user_id):
    """Send email to confirmation account."""

    user = User.objects.filter(id=user_id).first()

    verification_token = verification_refresh_token(user)
    subject = f"Welcome @{user}, please verify your account then you will be redirected to your Lazygram profile."
    from_email = "Lazygram <noreply@lazygram.com>"
    html_content = render_to_string(
        "emails/users/account_verification.html",
        {"user": user, "token": verification_token},
    )
    msg = EmailMultiAlternatives(subject, html_content, from_email, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@app.task(name="send_forgot_password_email", max_retries=3)
def send_forgot_password_email(user_id):
    """Send email to recover password."""
    user = User.objects.filter(id=user_id).first()
    verification_token_ = verification_access_token(user)

    subject = f"@{user}, Has forgotten your password? Copy the access token and paste in the input."
    from_email = "Lazygram <noreply@lazygram.com>"
    html_content = render_to_string(
        "emails/users/forgot_password.html",
        {"user": user, "token": verification_token_},
    )
    msg = EmailMultiAlternatives(subject, html_content, from_email, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
