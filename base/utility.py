import re
import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
regex_username = r'^[a-z0-9_.-]{3,15}$'


def check_email(email):
    if re.fullmatch(regex, email):
        return True

    else:
        return False


def check_username(username):
    if re.fullmatch(regex_username, username):
        return True

    else:
        return False


def check_user(user_input):
    if re.fullmatch(regex, user_input):
        return 'email'
    elif re.fullmatch(regex_username, user_input):
        return "username"
    else:
        return False


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']]
        )

        if data.get('content_type') == "html":
            email.content_subtype = 'html'

        EmailThread(email).start()


def send_email(email, code):
    html_content = render_to_string(
        'auth/send_email_code.html',
        {'code': code},
    )
    Email.send_email(
        {
            'subject': 'youtubedan ruyxatdan otish',
            'body': html_content,
            'to_email': email,
            'content_type': 'html',
        }
    )