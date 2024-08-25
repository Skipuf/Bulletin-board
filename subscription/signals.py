from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SubscriptionMessages
from .tasks import send_email_subscriptions


@receiver(post_save, sender=SubscriptionMessages)
def comment_created(instance, created, **kwargs):
    if not created:
        return

    send_email_subscriptions.delay(instance.id)

