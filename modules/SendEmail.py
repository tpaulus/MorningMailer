#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

import smtplib
import mandrill  # If you don't want to use mandrill, comment out this line
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from properties import Property
import lib.requests as Requests



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
            self.sendgrid_username = Property.sg_username
            self.sendgrid_password = Property.sg_password

    def send(self, to, subject, message_html):
        data = dict()
        data['api_user'] = self.sendgrid_username
        data['api_key'] = self.sendgrid_password
        data['to'] = to
        data['from'] = Property.email_from
        data['subject'] = subject
        data['html'] = message_html
        sg_response = Requests.post('https://api.sendgrid.com/api/mail.send.json', data)

        if sg_response.json()['message'] == 'success':
            return True
        else:
            return False, sg_response.json()['message']


class Mandrill(object):
    def __init__(self, isTest=False):
        if isTest:
            key = Property.mandrill_test_key
        else:
            key = Property.mandrill_prod_key

        self.client = mandrill.Mandrill(key)

    def send(self, to, subject, message_html):
        try:
            message = {'auto_text': True,
                       'from_email': Property.email_from,
                       'from_name': 'Python',
                       'html': message_html,
                       'important': False,
                       'signing_domain': Property.email_from.split('@')[1],
                       'subject': subject,
                       'tags': ['Morning Mailer'],
                       'to': [{'email': Property.email_to,
                               'name': Property.email_to_name,
                               'type': 'to'}],
                       'track_opens': True}

            result = self.client.messages.send(message=message)

            if result[0]['status'] == 'sent':
                return True
            else:
                return False, result[0]['reject_reason']

        except mandrill.Error, e:
            # Mandrill errors are thrown as exceptions
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
            raise

if __name__ == '__main__':
    # Email = smtp()
    # Email = SendGrid()
    Email = Mandrill()
    test_email = raw_input("What is your email? ")
    message = 'Hello World,\n\tThis is a test!'
    if not Email.send(test_email, 'TEST', message):
        quit("Mail Send Error")
    else:
        print "Message Sent Successfully!"