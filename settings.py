import os

DATADOG_API_KEY = os.environ['DATADOG_API_KEY']
DATADOG_APP_KEY = os.environ['DATADOG_APP_KEY']
CHRONOS_URL = os.environ['CHRONOS_URL'].split(',')
UPDATE_INTERVAL = float(os.environ['UPDATE_INTERVAL'])
