from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.conf import settings

User = get_user_model()

@receiver(post_save, sender=User)
def user_create(sender, instance, created, **kwargs):
    if created:
        subject = 'welcome'
        message = 'welcome to twitter'
        from_email = "test@test.com"
        recipient_list = [instance.email]

        email = EmailMessage(subject, message, from_email, recipient_list)
        email.content_subtype = 'html' 
        with open("templates/accounts/welcome.html", "r") as f:
            html_body = f.read()
        email.body = html_body

        email.send()
        
        
