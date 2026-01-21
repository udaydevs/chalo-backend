"""Email service for reset password"""
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_reset_otp(data):
    """
    This function will take user data and send email
    """
    subject = "Password Reset Otp"
    from_email = settings.EMAIL_HOST_USER
    context = {
        'otp': str(data.otp),
        'expiry' : data.otp_exp
    }
    html_content = render_to_string("otp_email.html", context=context)
    send_mail(
        html_message=html_content,
        subject=subject,
        from_email=from_email,
        recipient_list=[data.email],
        message=None
    )
