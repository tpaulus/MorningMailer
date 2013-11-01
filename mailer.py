#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from properties import Property

class mail(object):
    def __init__(self):
        self.smtp_user = Property.email_login
        self.smtp_password = Property.email_password
        self.smtp_server = Property.email_server
        self.smtp_port = Property.email_port
        self.smtpserver = smtplib.SMTP(self.smtp_server, self.smtp_port)

    def send(self, to, subject, message):
        try:
            self.smtpserver.ehlo()
            self.smtpserver.starttls()
            self.smtpserver.ehlo()
            self.smtpserver.login(self.smtp_user, self.smtp_password)
            msg = MIMEText(message, 'html')
            msg['Subject'] = subject
            msg['From'] = Property.email_from
            msg['To'] = to
            msg['Date'] = formatdate(localtime=True)
            self.smtpserver.sendmail(self.smtp_user, [to], msg.as_string())
            self.smtpserver.quit()
            return True

        except smtplib.SMTPException:
            return False


if __name__ == '__main__':
    Email = mail()
    test_email = raw_input("What is your email? ")
    if Email.send(test_email, 'TEST', 'Hello World,\n\tThis is a test!'):
        pass
    else:
        quit("Mail Send Error")