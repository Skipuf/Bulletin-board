from datetime import timedelta

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.utils import timezone

from .models import User_key


@shared_task
def send_email_registration_user(user):
    user = User.objects.get(id=user)

    subject = 'Добро пожаловать!'
    text = (
        f'{user.username}, вы успешно зарегистрировались на сайте!\n\n'
        f'http://127.0.0.1:8000/'
    )
    html = (
        f'<b>{user.username}</b>, вы успешно зарегистрировались на '
        f'<a href="http://127.0.0.1:8000/">сайте</a>!<br><br>'
    )

    msg = EmailMultiAlternatives(
        subject=subject, body=text, from_email=None, to=[user.email]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()


@shared_task
def send_email_key_user(user):
    print(user)
    user = User.objects.get(id=user)
    key = User_key.objects.get(user_id=user)

    subject = 'Подтверждение почты!'
    text = (
        f'{user.username}, чтобы подтвердить свой адрес электронной почты, '
        f'введите код, указанный ниже, на нашем сайте.\n\n'
        f'Код: {key.key}\n\n'
        f'http://127.0.0.1:8000/'
    )
    html = (
        f'<b>{user.username}</b>, чтобы подтвердить свой адрес электронной почты, '
        f'введите код, указанный ниже, на нашем сайтe.<br><br>'
        f'Код: {key.key}<br><br>'
        f'<a href="http://127.0.0.1:8000/">Ссылка на сайт</a>'
    )

    msg = EmailMultiAlternatives(
        subject=subject, body=text, from_email=None, to=[user.email]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()


@shared_task
def clear_old():
    old_key = User_key.objects.all().exclude(timestamp__gt=timezone.now() - timedelta(minutes=10))
    old_key.delete()
