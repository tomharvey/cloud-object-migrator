import json

from migrate.copy import FileCopier
from migrate.config import config


def consume_queue(event, context):
    config.update_from_file('settings.py')
    fc = FileCopier()
    for record in event['Records']:
        body = json.loads(record['body'])
        print(body)
        fc.copy_files(body)
