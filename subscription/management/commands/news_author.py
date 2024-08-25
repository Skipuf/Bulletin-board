from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from subscription.models import SubscriptionMessages


class Command(BaseCommand):
    help = 'Команда для создания группы автора новостей'

    def handle(self, *args, **kwargs):
        group_name = 'Author news'

        group, created = Group.objects.get_or_create(name=group_name)

        content_type = ContentType.objects.get_for_model(SubscriptionMessages)

        permissions = Permission.objects.filter(content_type=content_type).filter(codename__in=[
            'add_subscriptionmessages',
            'change_subscriptionmessages',
            'delete_subscriptionmessages',
            'view_subscriptionmessages',
        ])

        group.permissions.set(permissions)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана и разрешения назначены.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" уже существует. Разрешения обновлены.'))