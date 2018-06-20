from datadog import initialize, api
from settings import *
import chronos
from marathon import MarathonClient
import logging


def send_dd_event(title, text, tags, source_type, alert_type='info'):
    """Sends events to datadog"""

    options = {
        'api_key': DATADOG_API_KEY,
        'app_key': DATADOG_APP_KEY
    }

    initialize(**options)

    api.Event.create(title=title,
                     text=text,
                     tags=tags,
                     alert_type=alert_type,
                     source_type_name='chronos'),

def get_chronos_services_health(chronos_url):
    """Gets health of all services from chronos"""
    client = chronos.connect(chronos_url)
    for job in client.list():
        if job['errorsSinceLastSuccess'] is not 0:
            send_dd_event("Chronos task: {} failed".format(job['name']),
                          "Chronos Task Id: {}\nLast success: {}\nLast error: {}".format(job['name'], job['lastSuccess'], job['lastError']),
                          generate_tags('chronos', job['name']),
                          "chronos",
                          "error"
                         )
        else:
            send_dd_event("Chronos task: {} ran succesfully".format(job['name']),
                          "Chronos Task Id: {}\nLast success: {}\nLast error: {}".format(job['name'], job['lastSuccess'], job['lastError']),
                          generate_tags('chronos', job['name']),
                          "chronos",
                         )

def get_marathon_services_health(marathon_url):
    """Gets health of all services from marathon"""
    client = MarathonClient(marathon_url)
    for app in client.list_apps(embed_tasks=True):
        if app.tasks_unhealthy > 0:
            unhealthy_tasks = []
            for task in app.tasks:
                if task.state == "TASK_RUNNING" or task.state == "TASK_STAGING":
                    continue
                else:
                    unhealthy_tasks.append(task.id)
            send_dd_event("Marathon service: {} has failed tasks".format(app.id),
                          "Id: {}\nRunning Tasks: {}\nUnhealthy Tasks: {}\nUnhealthy Task IDs: {}\n".format(app.id, app.tasks_running, app.tasks_unhealthy, unhealthy_tasks),
                          generate_tags('marathon', app.id),
                          "marathon",
                          "error"
                         )
        else:
            send_dd_event("Marathon service: {} healthy".format(app.id),
                          "Id: {}\nRunning Tasks: {}\nUnhealthy Tasks: {}".format(app.id, app.tasks_running, app.tasks_unhealthy),
                          generate_tags('marathon', app.id),
                          "marathon",
                         )

def generate_tags(framework, task_name):
    """Generates tags to send to datadog"""
    return [framework, task_name]
