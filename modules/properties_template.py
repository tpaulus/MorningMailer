# TODO Add instructions for user on how to properly use this file and its necessary renaming

from copy import deepcopy


class Const(object):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            return deepcopy(self.__dict__[name])
        self.__dict__[name] = value

    def __getattr__(self, name, value):
        if name in self.__dict__:
            return deepcopy(self.__dict__[name])

    def __delattr__(self, item):
        if item in self.__dict__:
            pass


Property = Const()
Property.Version = 1
#
#   Web URLS
#
Property.root_path = ''
Property.root_web_path = ''
Property.header = 'header'
#
#   API Tokens
#
Property.wunderground = ''
Property.nyt = ''
#
#   Todoist
#
Property.todoist_email = ''
Property.todoist_password = ''
#
#   Email
#
Property.email_template_loc = './modules/email_template.html'
Property.email_result_loc = './email.html'
Property.email_log_loc = './email_tidy.log'
Property.email_to = ''
Property.email_to_name = 'John Doe'
Property.email_subject = 'Good Morning'
Property.email_server = ''
Property.email_port = 0
Property.email_from = ''
Property.email_login = ''
Property.email_password = ''
#
#   Sendgrid API (Alternative to SMPT)
#
Property.sg_username = ''
Property.sg_password = ''
#
#   Mandrill API (Alternative to SMPT)
#
Property.mandrill_test_key = ''
Property.mandrill_prod_key = ''
#
#   User Info
#
Property.user_TimeZone = ''
Property.user_city = ''
Property.user_state = ''

Property.send_email = True