from celery import shared_task
from datetime import timezone, datetime, timedelta
from .models import Category, Post, User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def mail_new_post(id, created):
    if created:
        post = Post.objects.get(pk=id)
        subscribers = list(
            post.postCategory.all().values_list('subscribers', flat=True))  # вынимаем список с id подписчиков
        subject = f'Новая статья в категории {post.category}'
        for user_id in subscribers:
            user = User.objects.get(id=user_id)
            email = user.email
            html_content = render_to_string(
                'mail_new_post_for_subscribers.html',
                {
                    'text': post.text,
                    'title': post.title,
                    'category': post.category,
                    'username': user.username,
                    'link': f'http://127.0.0.1:8000/news/{post.id}',
                })
            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=' ',
                to=[email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def weekly_email():
    timer = datetime.now(timezone.utc)
    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        posts = Post.objects.filter(postCategory__pk=category.id, dateCreation__gte=(timer - timedelta(days=2)))
        cat = Category.objects.get(pk=category.id)
        for subscriber in subscribers:
            html_content = render_to_string(
                'weekly_posts.html',
                {
                    'user': subscriber,
                    'cat': cat,
                    'posts': posts,
                }
            )
            msg = EmailMultiAlternatives(
                subject='Посты за неделю',
                from_email='',
                to=[subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
