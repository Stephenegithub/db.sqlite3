from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import account_activation_token


@receiver(post_save, sender=User)
def sending_email_to_registered_user(sender, instance, created, **kwargs):
    if created:
        subject = 'SOFSMART Account Email Verification.'
        msg_plain = render_to_string('accounts/emails/email.txt')
        msg_html = render_to_string('accounts/emails/account_activation_email.html', {
            'user': instance,
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'token': account_activation_token.make_token(instance),
        })
        send_mail(subject, msg_plain, "SOFSMART Account Registration", [instance.email], html_message=msg_html)