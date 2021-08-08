from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsBlog import settings
from .models import Post, User


@receiver(post_save, sender=User)
def welcome_letter(sender, instance, created, **kwargs):
    if created:
        send_mail(subject=f' Привет, {instance.username}',
                  message=f' Привет, {instance.username}! Добро пожаловать!',
                  from_email='riveriswild.rw@gmail.com',
                  recipient_list=[instance.email]
                  )


