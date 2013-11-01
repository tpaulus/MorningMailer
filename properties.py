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
Property.root_path = '/home/tompaulu/public_html/img/'
Property.root_web_path = 'http://tompaulus.com/img/'
Property.news_url = 'news/'
Property.weather_url = 'weather/'
Property.header_url = 'header/'
#
#   API Tokens
#
Property.wunderground_api_key = 'ce9f51b4688cc056'
Property.nyt_api_key = 'aceccc7823a34de46d5268e4a196ec17:14:68278972'
#
#   Todoist
#
Property.todoist_email = 'tom@tompaulus.com'
Property.todoist_password = 'tp ToDo !'
#
#   Email
#
Property.email_to = 'tom@tompaulus.com'
Property.email_subject = 'Good Morning'
Property.email_server = 'mail.tompaulus.com'
Property.email_port = 26
Property.email_from = 'Python<python@tompaulus.com>'
Property.email_login = 'python@tompaulus.com'
Property.email_password = 'MontyPyth0n'
#
#   User Info
#
Property.user_TimeZone = ''
Property.user_city = 'Ramona'
Property.user_state = 'CA'

Property.on_server = True