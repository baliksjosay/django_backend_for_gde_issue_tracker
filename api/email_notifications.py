from django.core.mail import send_mail
from Issue_tracker.settings import EMAIL_HOST_USER 

class EmailNotification:
    def __init__(self, subject, message, to):
        self.subject = subject
        self.message = message
        self.to = to

    def send(self):
        send_mail(
            self.subject,
            self.message,
            EMAIL_HOST_USER,
            [self.to],
            fail_silently=False,
        )



