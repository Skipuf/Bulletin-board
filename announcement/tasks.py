from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from .models import Comment


@shared_task
def send_email_comment(comment):
    comment = Comment.objects.get(id=comment)
    user_receive = User.objects.get(id=comment.post.author.id)
    user_send = User.objects.get(id=comment.author.id)

    subject = 'Вы получили ответ на ваше объявление!'
    text = (
        f'Здравствуйте, {user_receive.username}.\n'
        f'Вы получили ответ на ваше объявление "{comment.post.title}", '
        f'от пользователя {user_send.username}.\n\n'
        f'Ответ: {comment.text}\n\n'
        f'Ждем вас на нашем портале: http://127.0.0.1:8000/'
    )
    html = (
        f'Здравствуйте, <b>{user_receive.username}</b><br>'
        f'Вы получили ответ на ваше объявление "{comment.post.title}", '
        f'от пользователя <b>{user_send.username}</b>.<br><br>'
        f'Ответ: {comment.text}<br><br>'
        f'Ждем вас на нашем портале: <a href="http://127.0.0.1:8000/">ссылка</a>!'
    )

    msg = EmailMultiAlternatives(
        subject=subject, body=text, from_email=None, to=[user_receive.email]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()


@shared_task
def send_email_comment_accept(comment: Comment):
    comment = Comment.objects.get(id=comment)
    user = User.objects.get(id=comment.author.id)

    subject = 'Ваш ответ приняли!'
    text = (
        f'Здравствуйте, {user.username}.\n'
        f'Ваш ответ на объявление "{comment.post.title}", принят!\n\n'
        f'Ждем вас на нашем портале: http://127.0.0.1:8000/'
    )
    html = (
        f'Здравствуйте, <b>{user.username}</b><br>'
        f'Ваш ответ на объявление "{comment.post.title}", принят!<br><br>'
        f'Ждем вас на нашем портале: <a href="http://127.0.0.1:8000/">ссылка</a>!'
    )

    msg = EmailMultiAlternatives(
        subject=subject, body=text, from_email=None, to=[user.email]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()