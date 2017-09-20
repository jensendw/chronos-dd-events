import os

DATADOG_API_KEY = os.environ['DATADOG_API_KEY']
DATADOG_APP_KEY = os.environ['DATADOG_APP_KEY']

if os.environ.get('CHRONOS_URL') is not None:
    CHRONOS_URL = os.environ['CHRONOS_URL'].split(',')
else:
    CHRONOS_URL = None

if os.environ.get('MARATHON_URL') is not None:
    MARATHON_URL = os.environ['MARATHON_URL'].split(',')
else:
    MARATHON_URL = None

UPDATE_INTERVAL = float(os.environ.get('UPDATE_INTERVAL', 60))
