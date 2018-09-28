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
        self.aws = boto3.resource('s3')

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
        service, file_path = source.split(":")
        if service == "cloudfiles":
            body = self._get_from_rackspace(file_path)
        if service == "s3":
            body = self._get_from_aws(file_path)
        else:
            raise NotImplementedError
        return body

    def put_destination(self, destination, source_content):
        """Upload content to the destination."""
        service, destination_path = destination.split(":")
        if service == "s3":
            success = self._put_to_aws(destination_path, source_content)
        else:
            raise NotImplementedError
        return success

    def _get_from_rackspace(self, file_path):
        """Get the content from rackspace."""
        obj_name, container_name = self._parse_file_dir_name(file_path)
        response = self.rackspace.object_store.download_object(
            obj_name, container=container_name)
        return response

    def _get_from_aws(self, file_path):
        """Get the content from AWS S3."""
        key_name, bucket_name = self._parse_file_dir_name(file_path)
        s3_object = self.aws.Object(bucket_name, key_name)
        response = s3_object.get()
        body = response['Body'].read()
        return body

    def _put_to_aws(self, destination_path, source_content):
        """Put the contents into AWS S3."""
        key_name, bucket_name = self._parse_file_dir_name(destination_path)
        s3_object = self.aws.Object(bucket_name, key_name)
        s3_object.put(
            Body=source_content,
            ContentType="image/jpeg",
            StorageClass="STANDARD_IA"
        )
        return True

    def _parse_file_dir_name(self, file_path):
        """Get the name of the file/key and object/container."""
        _, _, container_name, *file_parts = file_path.split("/")
        obj_name = "/".join(file_parts)
        return obj_name, container_name
