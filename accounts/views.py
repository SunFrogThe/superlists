from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest
from django.core.mail import send_mail
from django.contrib import messages

from .models import Token

SUBJECT = 'Your login link for Superlists'
BODY = 'Use this link to log in:\n\n'
FROM_EMAIL = 'noreply@superlists'
MESSAGE = "Check your email, we've sent you a link you can use to log in."


def send_login_email(request: HttpRequest):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        f"{reverse('login')}?token={token.uid}"
    )
    message_body = f'{BODY}{url}'
    send_mail(
        SUBJECT,
        message_body,
        FROM_EMAIL,
        [email],
    )
    messages.success(request, MESSAGE)
    return redirect('/')


def login(request: HttpRequest):
    token = request.GET['token']
    return redirect('/')
