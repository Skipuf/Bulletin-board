from random import choice

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def gen_key():
    list_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                 '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    password = ''
    for number in range(5):
        password += choice(list_char)
    return password


class User_login(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)


class User_key(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.TextField(default=gen_key)
    timestamp = models.DateTimeField(default=timezone.now)
