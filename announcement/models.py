import bleach
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


class Post(models.Model):
    POSITIONS = [
        ('tank', 'Танк'),
        ('hill', 'Хил'),
        ('dd', 'ДД'),
        ('dealer', 'Торговец'),
        ('guildmaster', 'Гилдмастер'),
        ('questgiver', 'Квестгивер'),
        ('blacksmith', 'Кузнец'),
        ('tanner', 'Кожевник'),
        ('potion_master', 'Зельевар'),
        ('spell_master', 'Мастер Заклинаний'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=13,
                                 choices=POSITIONS,
                                 default='tank')
    title = models.CharField(max_length=200)
    content = HTMLField()
    status = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Очищаем HTML перед сохранением
        allowed_tags = [
            'p', 'b', 'i', 'u', 'a', 'img', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'br', 'span', 'div', 'blockquote',
            'pre', 'code', 'strong', 'em'
        ]
        allowed_attributes = {
            '*': ['class', 'style', 'strong', 'em'],
            'a': ['href', 'title', 'target'],
            'img': ['src', 'alt'],
        }
        self.content = bleach.clean(self.content, tags=allowed_tags, attributes=allowed_attributes)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=11,
                              choices=[
                                  ('Accepted', "Принято"),
                                  ('Rejected', "Отклонено"),
                                  ('Not defined', 'Не определено')
                              ],
                              default='Not defined')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
