from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment
from .tasks import send_email_comment, send_email_comment_accept


@receiver(post_save, sender=Comment)
def comment_created(instance, created, **kwargs):
    if not created:
        if instance.status == "Accepted":
            send_email_comment_accept.delay(instance.id)
    else:
        send_email_comment.delay(instance.id)

