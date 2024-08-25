from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User_login, User_key
from .tasks import send_email_key_user, send_email_registration_user


@receiver(post_save, sender=User)
def comment_created(instance, created, **kwargs):
    if not created:
        return

    User_login.objects.create(user_id=instance)
    send_email_registration_user.delay(instance.id)
    User_key.objects.create(user_id=instance)


@receiver(post_save, sender=User_key)
def comment_created(instance, created, **kwargs):
    if not created:
        return

    send_email_key_user.delay(instance.user_id.id)

