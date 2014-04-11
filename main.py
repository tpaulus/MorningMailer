#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

from __future__ import unicode_literals
import os
import random
from modules.parse import Greeting
from modules.SendEmail import *
from modules.wunderground import *
from modules.todoist import *
from modules.nyt import *
from modules.properties import Property
from modules.html import GenEmail


class main(object):
    def __init__(self, send_email=True):
        self.send_email = send_email

    @classmethod
    def greeting(cls):
        p = Greeting()
        p.get()
        return p.get_random()

    @classmethod
    def weather(cls):
        w = Weather()
        text, icon = w.get_forecast()
        map_URL = w.get_map_url()
        return text, icon, map_URL

    @classmethod
    def todo(cls):
        t = Todos()
        task_list = t.get()
        section = '<dl>\n'
        for task in task_list:
            due = task.parsed_date()
            project = task.project
            text = task.name + ', Due: ' + due + ' - <font color=%s>' % project.color + project.name + '</font>'
            if task.priority == 4:
                color = ' style="color: #B8412B"'
            elif task.priority == 3:
                color = ' style="color: #3363A4"'
            elif task.priority == 2:
                color = ' style="color: #8EC4FF"'
            else:
                color = ''

            section += '<dt%s> %s </dt>\n' % (color, text)
            if task.notes != tuple():
                for note in task.notes:
                    section += '<dd>- %s </dd>\n' % note

        section += '</dl>'
        if section == '<dl></dl>':
            section = "You're good! Nothing todo in the next few days."
        return section

    @classmethod
    def news(cls):
        news = TopStories()
        articles = news.get(4)
        return articles

    @classmethod
    def send(cls, email_message_location):
        email = mail()
        with open(email_message_location, 'r') as email_message:
            if email.send(Property.email_to, Property.email_subject, email_message.read()):
                pass
            else:
                quit("Mail Send Error")

    def customize_email(self):
        header_image = '%s%s%d.jpg' % (Property.root_web_path, Property.header_url, random.randint(0, 10))

        language, greeting = self.greeting()
        date = datetime.now().strftime("%A, %B %d, %Y")

        weather_text, weather_icon, weather_radar = self.weather()
        weather_text = 'It will be ' + weather_text

        todo_list = self.todo()

        article_list = self.news()

        # Begin Email Message Content
        message = GenEmail()
        message.title = 'Good Morning'
        message.summary = {'text': weather_text}
        message.header_image = {'url': header_image}
        message.body_r1 = {'title': greeting + ", that's " + language + ' for Good Morning!',
                           'subtitle': 'Today is ' + date + '.', 'text': weather_text}
        message.body_image = {'url': weather_radar}
        message.body_r2 = {'title': 'Todoist Tasks', 'subtitle': 'Tasks due in the next 3 to 4 days.',
                           'text': todo_list}

        for a in range(0, len(article_list)):
            url = article_list[a].image
            title = article_list[a].title
            text = article_list[a].content
            message.columns.append({'url': url, 'title': title, 'text': text})

        message.generate()  # Send

    def finalize(self):
        if Property.send_email and self.send_email:
            self.send(Property.email_save_loc)
        else:
            print "No email was sent, because you told me not to. Check email.html for your email message."

if __name__ == '__main__':
    m = main()
    m.customize_email()
    m.finalize()