from datadog import initialize, api
from settings import *
import chronos

def send_dd_event(title, text, tags, alert_type='info'):
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

def get_services_health(chronos_url):
    """Gets health of all services from chronos"""
    client = chronos.connect(chronos_url)
    for job in client.list():
        if job['errorsSinceLastSuccess'] is not 0:
            send_dd_event("Chronos task: {} failed".format(job['name']),
                          "Chronos Task Id: {}\nLast success: {}\nLast error: {}".format(job['name'], job['lastSuccess'], job['lastError']),
                          generate_tags(job['name']),
                          "error"
                         )
        else:
            send_dd_event("Chronos task: {} ran succesfully".format(job['name']),
                          "Chronos Task Id: {}\nLast success: {}\nLast error: {}".format(job['name'], job['lastSuccess'], job['lastError']),
                          generate_tags(job['name']),
                         )

def generate_tags(task_name):
    """Generates tags to send to datadog"""
    return ['chronos', task_name]
