from django.core.mail import send_mail
# from KaziYangu.settings import EMAIL_HOST_USER
from django.conf import settings

def send_mail_to(subject, message, receivers):
    send_mail(subject,message,EMAIL_HOST_USER,[RECIPIENT_ADDRESS],
    fail_silently= False)