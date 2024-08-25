from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from accounts.models import User_login
from .models import SubscriptionMessages


@shared_task
def send_email_subscriptions(sub):
    sub = SubscriptionMessages.objects.get(pk=sub)
    users = User_login.objects.filter(is_subscribed=True)

    subject = sub.title
    text = sub.text

    for user in users:
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.user_id.email]
        )
        msg.send()