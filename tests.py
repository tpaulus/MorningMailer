__author__ = 'tpaulus'

import unittest

try:
    from teamcity import is_running_under_teamcity
    from teamcity.unittestpy import TeamcityTestRunner
except ImportError:
    pass

import lib.requests as Requests

from modules.parse import *
from modules.html import *
from modules.nyt import *
from modules.properties import *
from modules.SendEmail import *
from modules.todoist import *
from modules.wunderground import *


def file_len(file_name):
    i = 0
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def exists(url):
    try:
        pkg = Requests.get(url)
        if pkg.status_code != 200:
            return False
    except:
        return False
    else:
        return True


class Parse(unittest.TestCase):
    def test_load(self):
        """Load the CSV file and parse it."""
        p = Greeting()
        keys = p.get()
        self.assertAlmostEqual(len(keys), file_len('./modules/good_morning.csv'), places=2)

    def test_dict(self):
        """Check to see if a dictionary was created and that it has values."""
        p = Greeting()
        p.get()
        self.assertTrue(type(p.get_dict()) is dict)
        self.assertTrue(len(p.get_dict().values()) > 0)

    def test_random(self):
        """Test to check if the Random function is random."""
        l = list()
        p = Greeting()
        p.get()
        for i in xrange(20):
            random_output = p.get_random()
            l.append(random_output)
            self.assertFalse(l.count(random_output) == 0)


class EmailMaker(unittest.TestCase):
    def test_articles(self):
        message = GenEmail()
        paper = TopStories()
        article_list = paper.pull(4)
        for a in range(0, len(article_list)):
            url = article_list[a].image
            title = article_list[a].title
            text = article_list[a].content
            message.columns.append({'url': url, 'title': title, 'text': text})
        message.generate()

        with open('./email.html') as generated:
            text = generated.read()
            article_count = text.count('<td class="leftColumnContent">')
            article_count += text.count('<td class="rightColumnContent">')

        self.assertEqual(len(article_list), article_count)


class NYT(unittest.TestCase):
    def test_stories(self):
        paper = TopStories()
        news = paper.pull(10)
        self.assertNotEqual(news, False)
        self.assertTrue(len(news) <= 10)
        for story in news:
            self.assertTrue(story.image is not None)
            self.assertTrue(exists(story.image))
            self.assertTrue(story.title is not None)
            self.assertTrue(type(story.title) == str or type(story.title) == unicode)
            self.assertTrue(story.content is not None)
            self.assertTrue(type(story.content) == str or type(story.content) == unicode)


class Email(unittest.TestCase):
    def test_send_smtp(self):
        Email = smtp()
        to = 'smtp_test@ramonatechguys.com'
        message = 'Hello World,\n\tThis is a test!'
        self.assertTrue(Email.send(to, 'TEST', message))

    def test_send_sendgrid(self):
        Email = SendGrid()
        to = 'smtp_test@ramonatechguys.com'
        message = 'Hello World,\n\tThis is a test!'
        self.assertTrue(Email.send(to, 'TEST', message))

    def test_mandrill(self):
        Email = Mandrill(isTest=True)
        to = 'smtp_test@ramonatechguys.com'
        message = 'Hello World,\n\tThis is a test!'
        self.assertTrue(Email.send(to, 'TEST', message))

class Properties(unittest.TestCase):
    pass


class Todoist(unittest.TestCase):
    def test_login(self):
        email = Property.todoist_email
        password = Property.todoist_password
        t = Todos.login(email, password)
        self.assertFalse(t['token'] is None)

    def test_get_projects(self):
        t = Todos()
        projects = t.get_projects()
        self.assertNotEqual(projects, [], msg="No Projects")
        for project in projects:
            self.assertNotEqual(project.id, 0, msg="No ID")
            self.assertNotEqual(project.name, '', msg="No Project Name")

    def test_get_tasks(self):
        pass

    def test_get_near(self):
        pass


class WeatherUnderground(unittest.TestCase):
    def test_get_data(self):
        weather = Weather()
        data = weather.get_data()
        self.assertTrue(data is not False or data is not None)
        self.assertTrue(type(data) == dict)

    def test_weather_test(self):
        weather = Weather()
        forecast, weather_icon = weather.get_forecast()
        self.assertTrue(type(forecast) == str)
        if weather_icon != '':
            self.assertTrue(exists(weather_icon))

    def test_radar_map(self):
        weather = Weather()
        weather.get_forecast()
        url = weather.get_map_url()
        self.assertTrue(exists(url))


if __name__ == '__main__':
    try:
        if is_running_under_teamcity():
            runner = TeamcityTestRunner()
        else:
            runner = unittest.TextTestRunner()
        unittest.main(testRunner=runner)

    except Exception:
        unittest.main()