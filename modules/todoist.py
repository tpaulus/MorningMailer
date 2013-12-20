#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

import sys

from datetime import datetime, timedelta
from lib.dateutil import tz

import lib.requests as Requests
from properties import Property

reload(sys)
sys.setdefaultencoding("utf-8")


class Task(object):
    p_index = {4: 'Highest',
               3: 'High',
               2: 'Medium',
               1: 'Low'}

    def __init__(self, name, project, due, priority):
        self.name = name
        self.project = project
        self.due = due
        self.priority = priority

    def __str__(self):
        due = datetime.strftime(self.due, '%a %d %b %Y %H:%M:%S %Z')
        string = self.name + ' - ' + self.project + ', Due: ' + due + '- P: ' + Task.p_index[self.priority]
        #string = self.name + ', Due: ' + due + ' - ' + self.project
        return string


class Todos(object):
    def __init__(self, email, password):
        auth = Requests.get('https://todoist.com/API/login?email=' + email + '&password=' + password).json()
        self.token = auth['token']
        self.p_ids = []
        self.projects = {}
        self.tasks = []
        self.timeZone = auth['timezone']
        Property.user_TimeZone = self.timeZone

    def get_projects(self):
        p_list = Requests.get('https://todoist.com/API/getProjects?token=' + self.token).json()
        for num in range(0, len(p_list)):
            name = p_list[num]['name']
            id = p_list[num]['id']
            self.p_ids.append(id)
            self.projects[name] = id
            self.projects[id] = name

    def get_tasks(self):
        for id in self.p_ids:
            project_tasks = Requests.get(
                'https://todoist.com/API/getUncompletedItems?project_id=' + str(id) + '&token=' + self.token).json()
            for task_num in range(0, len(project_tasks)):
                date_string = str(project_tasks[task_num]['due_date'].strip())
                if date_string.find('.') > -1:
                    date_string = date_string[0:date_string.find('.')]
                if date_string.find('+') > -1:
                    date_string = date_string[0:date_string.find('+')]

                try:
                    utc = datetime.strptime(date_string, '%a %d %b %Y %X')
                except ValueError:
                    try:
                        utc = datetime.strptime(date_string, '%a %d %b %Y %X ')
                    except ValueError:
                        try:
                            utc = datetime.strptime(date_string, '%a %b %d %Y %X %z')
                        except ValueError:
                            utc = datetime(1900, 1, 1)
                            #print 'input:', date_string, 'processed:', utc

                utc = utc.replace(tzinfo=tz.gettz('UTC'))
                local = tz.gettz(self.timeZone)  # set a fixed TimeZone
                #local = tz.tzlocal()   # Use to auto-detect local TimeZone
                date_due = utc.astimezone(local)

                task = project_tasks[task_num]['content'].replace('*', '')
                priority = project_tasks[task_num]['priority']

                new_task = Task(task, self.projects[id], date_due, priority)
                self.tasks.append(new_task)

    def near(self, delta):
        near = []
        td = timedelta(days=delta)
        now = datetime.now(tz.gettz(self.timeZone))
        for task in self.tasks:
            if task.due - now < td:
                near.append(task)
        near.sort(key=lambda r: r.due)

        return near

    def get(self, delta=4):
        self.get_projects()
        self.get_tasks()
        return self.near(delta)


if __name__ == '__main__':
    login = raw_input("Todoist User Name: ")
    password = raw_input("Password: ")
    t = Todos(login, password)
    task_list = t.get()
    for task in task_list:
        print task