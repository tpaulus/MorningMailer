#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from properties import Property
<<<<<<< HEAD
import requests as Requests

=======
import requests
>>>>>>> hotfix/2.5.1


class smtp(object):
    def __init__(self):
        self.smtp_user = Property.email_login
        self.smtp_password = Property.email_password
        self.smtp_server = Property.email_server
        self.smtp_port = Property.email_port
        self.smtpserver = smtplib.SMTP(self.smtp_server, self.smtp_port)

    def send(self, to, subject, message_html):

        try:
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = subject
            msgRoot['From'] = Property.email_from
            msgRoot['To'] = to
            msgRoot['Date'] = formatdate(localtime=True)

            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)

            # TODO add plaintext attachment to the email
            # msgText = MIMEText(message_plain, _charset='utf-8')
            # msgAlternative.attach(msgText)

            msgText = MIMEText(message_html, 'html', _charset='utf-8')
            msgAlternative.attach(msgText)

            self.smtpserver.ehlo()
            self.smtpserver.starttls()
            self.smtpserver.ehlo()
            self.smtpserver.login(self.smtp_user, self.smtp_password)
            self.smtpserver.sendmail(self.smtp_user, [to], msgRoot.as_string())
            self.smtpserver.quit()
            return True

        except smtplib.SMTPException:
            return False


class SendGrid(object):
    def __init__(self):
        self.key = Property.sg_api_key

    def send(self, to, subject, message_html):
        data = dict()
        data['to'] = to
        data['toname'] = Property.email_to_name
        data['from'] = Property.email_from
        data['fromname'] = Property.email_from_name
        data['subject'] = subject
        data['html'] = message_html

        session = requests.Session()
        session.headers.update({'Authorization': 'Bearer ' + self.key})
        sg_response = session.post('https://api.sendgrid.com/api/mail.send.json', data)

        if sg_response.json()['message'] == 'success':
            return True
        else:
            return False, sg_response.json()['message']


if __name__ == '__main__':
    # Email = smtp()
    Email = SendGrid()
    test_email = raw_input("What is your email? ")
    message = 'Hello World,\n\tThis is a test!'
    if not Email.send(test_email, 'TEST', message):
        quit("Mail Send Error")
    else:
        print "Message Sent Successfully!"