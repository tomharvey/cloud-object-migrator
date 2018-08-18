"""Copy the files in a message."""
from rackspace import connection
import boto3

from migrate.config import config


class FileCopier():
    """Handle the file copying."""

    def __init__(self):
        """Setup clients for Rackspace and AWS."""
        self.rackspace = connection.Connection(
            username=config.RACKSPACE_USER,
            api_key=config.RACKSPACE_API,
            region=config.RACKSPACE_REGION)
        self.aws = boto3.client('s3')

    def copy_files(self, message):
        """Copy files from source to destination."""
        files = message['files']
        source = files['source']
        destination = files['destination']

        source_content = self.get_source(source)
        success = self.put_destination(destination, source_content)
        return success

    def get_source(self, source):
        """Get the content of the source file."""
        service, file = source.split(":")
        if service == "cloudfiles":
            header, body = self._get_source_from_rackspace(file)
        if service == "s3":
            body = self._get_source_from_aws(file)
        return body

    def put_destination(self, destination, source_content):
        """Upload content to the destination."""
        print(destination)
        print(source_content)
        return True

    def _get_source_from_rackspace(self, file):
        """Get the content from rackspace."""
        _, _, container, *file_parts = file.split("/")
        obj = "/".join(file_parts)
        response = self.rackspace.get_object(container, obj)
        return response

    def _get_source_from_aws(self, file):
        """Get the content from AWS."""
        print(file)
        return "aws"
