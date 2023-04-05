from django.core.mail import send_mail
import random
from django.conf import settings
from .models import Patient


def generate_otp():
    return random.randint(100000, 999999)


def send_otp_via_email(email):

    subject = 'Verify your email for MLI'
    otp = generate_otp()
    message = f'Your otp is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    patient_obj = Patient.objects.get(email=email)
    patient_obj.otp = otp
    patient_obj.save()