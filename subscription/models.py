from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class SubscriptionMessages(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    data_published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_list')