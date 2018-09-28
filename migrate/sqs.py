import boto3
import botocore
import json

from migrate.config import config
from migrate.copy import FileCopier


class Sqs():
    """Aws SQS handler."""

    def __init__(self):
        """Create a class to handle SQS comms."""
        sqs = boto3.resource('sqs', region_name=config.AWS_REGION)
        queue_name = config.QUEUE_NAME
        try:
            sqs.create_queue(QueueName=queue_name, Attributes={
                'DelaySeconds': '5'
            })
        except:
            pass
        self.queue = sqs.get_queue_by_name(QueueName=queue_name)

    def add_message(self, file_pair, extras=None):
        """Add a message to SQS."""
        body = {
            'files': file_pair,
        }
        if extras:
            body['extras'] = dict(extras)
        message_body = json.dumps(body)
        self.queue.send_message(MessageBody=message_body)

    def consume_queue(self):
        """Consume the queue."""
        fc = FileCopier()
        while True:
            for message in self.queue.receive_messages(MaxNumberOfMessages=10):
                if fc.copy_files(json.loads(message.body)):
                    message.delete()
