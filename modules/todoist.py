#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

import sys

from datetime import datetime, timedelta
from lib.dateutil import tz

import lib.requests as Requests
from properties import Property

reload(sys)
sys.setdefaultencoding("utf-8")


class Project(object):
    color_index = ["#bde876", "#ff8581", "#ffc472", "#faed75", "#a8c9e5", "#999999", "#e3a8e5", "#dddddd", "#fc603c",
                   "#ffcc00", "#74e8d4", "#3cd6fc"]

    def __init__(self, id, name):
        """

        @param id: The Projects Unique ID
        @type id: int
        @param name: Name of the Project
        @type name: str
        """
        self.id = id
        self.name = name
        self.color = 0
        self.item_order = 1
        self.indent = 1



class Task(object):
    p_index = {4: 'Highest',
               3: 'High',
               2: 'Medium',
               1: 'Low'}

    def __init__(self, name, project, due, delta, priority, notes=tuple()):
        self.name = name
        self.project = project
        self.due = due
        self.delta = delta
        self.priority = priority
        self.notes = notes

    def __str__(self):
        due = datetime.strftime(self.due, '%a %d %b %Y %H:%M:%S %Z')
        string = self.name + ' - ' + self.project + ', Due: ' + due + '- P: ' + Task.p_index[self.priority]
        return string

    def parsed_date(self):
        parsed_date = ''
        if self.delta < timedelta(0):
            if self.delta.days >= -1:
                parsed_date = 'Yesterday'
            else:
                num_days = self.delta.days
                parsed_date = str(abs(num_days)) + ' Days Ago'
        elif self.delta.days < 2:
            if self.delta.days < 1:
                parsed_date = 'Today'
            elif self.delta.days < 2:
                parsed_date = 'Tomorrow'
        else:
            parsed_date = datetime.strftime(self.due, '%A, %b %d')
        return parsed_date


class Todos(object):
    @classmethod
    def login(cls, email, password):
        try:
            url = 'https://todoist.com/API/login?email=%s&password=%s' % (email, password)
            package = Requests.get(url)
            auth = package.json()
        except:
            auth = ''
            quit('Todoist was unable to login!')
        return auth

    def __init__(self):
        auth = Todos.login(Property.todoist_email, Property.todoist_password)
        self.token = auth['token']
        self.projects = []
        self.tasks = []
        self.timeZone = auth['timezone']
        Property.user_TimeZone = self.timeZone
        self.todoist_premium_status = auth['is_premium']

    def get_projects(self):
        try:
            url = 'https://todoist.com/API/getProjects?token=%s' % self.token
            package = Requests.get(url)
            p_list = package.json()
        except:
            p_list = ''
            quit('Todoist was unable to fetch the list of projects!')

        for num in range(0, len(p_list)):
            name = p_list[num]['name']
            project_id = int(p_list[num]['id'])
            new_project = Project(project_id, name)
            new_project.color = p_list[num]['color']
            new_project.item_order = p_list[num]['item_order']
            new_project.indent = p_list[num]['indent']

            self.projects.append(new_project)

        return self.projects

    def get_tasks(self):
        url = ''
        package = ''
        for project in self.projects:
            project_id = project.id
            try:
                url = 'https://todoist.com/API/getUncompletedItems?project_id=' + str(
                    project_id) + '&token=' + self.token
                package = Requests.get(url)
                project_tasks = package.json()
            except:
                print url
                print package.text
                continue

            for task_num in range(0, len(project_tasks)):
                task_id = int(project_tasks[task_num]['id'])
                # Correctly format and remove any extra characters that datetime can't handel

                if project_tasks[task_num]['due_date'] is None:
                    continue  # We don't care about tasks without due dates
                if int(project_tasks[task_num]['indent']) != 1:
                    # TODO Subtasks
                    continue  # Right now we can't handel Subtasks

                date_string = str(project_tasks[task_num]['due_date'].strip())
                if date_string == 'null':
                    continue
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
                            print 'input:', date_string, 'processed:', "Error"
                            continue  # Skip This Task, because it doesn't have a valid date and can't be sorted

                # Fix timezone, and set due date to local time zone
                utc = utc.replace(tzinfo=tz.gettz('UTC'))  # Default Todoist TZ is UTC
                local = tz.gettz(self.timeZone)  # set a fixed TimeZone, Which is set by the User in the Todoist App
                # local = tz.tzlocal()   # Use to auto-detect local TimeZone
                date_due = utc.astimezone(local)
                delta = date_due - datetime.now(tz=tz.gettz(self.timeZone))

                task_name = project_tasks[task_num]['content'].replace('*', '')
                task_priority = project_tasks[task_num]['priority']

                if self.todoist_premium_status:
                    package = ''
                    url = ''
                    task_notes = []
                    try:
                        url = 'https://todoist.com/API/getNotes?item_id=' + str(task_id) + '&token=' + self.token
                        package = Requests.get(url)
                        all_notes = package.json()
                        for note_number in range(0, len(all_notes)):
                            task_notes.append(all_notes[note_number]['content'])
                        task_notes = tuple(task_notes)

                    except:
                        task_notes = tuple()
                else:
                    task_notes = tuple()

                new_task = Task(task_name, project, date_due, delta, task_priority, task_notes)
                self.tasks.append(new_task)

    def near(self, delta):
        near = []
        td = timedelta(days=delta)
        now = datetime.now(tz.gettz(self.timeZone))
        for current_task in self.tasks:
            if current_task.due - now < td:
                near.append(current_task)
        near.sort(key=lambda r: r.due)

        return near

    def get(self, delta=4):
        self.get_projects()
        self.get_tasks()
        return self.near(delta)


if __name__ == '__main__':
    t = Todos()
    task_list = t.get()
    for task in task_list:
        print task