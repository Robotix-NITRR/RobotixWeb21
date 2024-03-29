from django.core.mail import EmailMessage, send_mail
import threading
from django.template.loader import render_to_string

from .models import CustomUser


class EmailThread(threading.Thread):

    def __init__(self, data):
        self.data = data
        threading.Thread.__init__(self)

    def run(self):
        html_message = render_to_string(
            'html_message.html', {'data' : self.data['email_link']}
        )
        send_mail(
            subject=self.data['email_subject'], message =self.data['email_body'],from_email=None, recipient_list=[self.data['to_email']], html_message=html_message)



class Util:
    @staticmethod
    def send_email(data):
        # html_message = render_to_string(
        #     'html_message.html', {'data' : data['email_link']}
        # )
        # send_mail(
        #     subject=data['email_subject'], message =data['email_body'],from_email=None, recipient_list=[data['to_email']], html_message=html_message)

        # email = EmailMessage(
        #     subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(data).start()

    @staticmethod
    def send_msg(data):
        pass
