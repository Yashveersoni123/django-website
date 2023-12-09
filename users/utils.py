from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_email_token(email, token):
    try:
        subject = "Your account needs to be verified"
        message = render_to_string('users/verification_email_template.html', {'token': token})
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        send_mail(
            subject,
            '',  # Plain text message (leave empty if sending only HTML)
            email_from,
            recipient_list,
            html_message=message,  # Set HTML content
        )

        return True

    except Exception as e:
        print(e)
        return False
    
def send_otp_token(email, otp_generate):
    try:
        subject = "Action Required: Reset Password"
        message = render_to_string('users/recovery_password_email.html', {'otp_generate': otp_generate})
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        send_mail(
            subject,
            '',  # Plain text message (leave empty if sending only HTML)
            email_from,
            recipient_list,
            html_message=message,  # Set HTML content
        )

        return True

    except Exception as e:
        print(e)
        return False
