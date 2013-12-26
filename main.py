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


def greeting():
    p = Greeting()
    p.get()
    return p.get_random()


def weather():
    w = Weather(Property.user_city, Property.user_state)
    w.get_data()
    text, icon = w.get_forecast()
    map_URL = w.get_map_url()
    download(Property.weather_url, "radar.gif", map_URL)
    return text, icon


def todo():
    t = Todos(Property.todoist_email, Property.todoist_password)
    task_list = t.get()
    section = '<dl>\n'
    for task in task_list:
        due = task.parsed_date()
        text = task.name + ', Due: ' + due + ' - ' + task.project
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


def news():
    news = TopStroies()
    articles = news.get(4)
    for num in range(len(articles)):
        download(Property.news_url, str(num + 1) + ".jpg", articles[num].image)
    return articles


def send(email_message_location):
    email = mail()
    with open(email_message_location, 'r') as email_message:
        if email.send(Property.email_to, Property.email_subject,  email_message.read()):
            pass
        else:
            quit("Mail Send Error")


def download(path, name, url):
    save_location = Property.root_path + path + name
    wget = "wget -qO %s %s" % (save_location, url)
    chmod = "chmod 644 %s" % save_location
    if Property.on_server:
        os.system(wget)
        os.system(chmod)



header_image = '%s%s%d.jpg' % (Property.root_web_path, Property.header_url, random.randint(0, 10))

language, greeting = greeting()
date = datetime.now().strftime("%A, %B %d, %Y")

weather_text, weather_icon = weather()
weather_text = 'It will be ' + weather_text

article_list = news()

# Begin Email Message Content
message = GenEmail()
message.title = 'Good Morning'
message.summary = {'text': weather_text}
message.header_image = {'url': header_image}
message.body_r1 = {'title': greeting + ", that's " + language + ' for Good Morning!',
                   'subtitle': 'Today is ' + date + '.', 'text': weather_text}
message.body_image = {'url': 'http://tompaulus.com/img/weather/radar.gif'}
message.body_r2 = {'title': 'Todoist Tasks', 'subtitle': 'Tasks due in the next 3 to 4 days.', 'text': todo()}


for a in range(0, len(article_list)):
    url = 'http://tompaulus.com/img/news/%d.jpg' % int((a+1))
    title = article_list[a].title
    text = article_list[a].content
    message.columns.append({'url': url, 'title': title, 'text': text})


message.generate()

if Property.send_email:
    send(Property.email_save_loc)
else:
    print "No email was sent, because you told me not to. Check email.html for your email message."
