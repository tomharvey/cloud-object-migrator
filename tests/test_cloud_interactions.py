from migrate.copy import FileCopier
from migrate.config import config


def test_get_from_rackspace():
    config.update_from_file('settings.py')
    fc = FileCopier()

    cloudfile = "cloudfiles://important_things/test.txt"

    service, file = cloudfile.split(":")
    assert service == "cloudfiles"

    body = fc._get_from_rackspace(file)

    assert body == b"test"


def test_put_to_aws():
    config.update_from_file('settings.py')
    fc = FileCopier()

    s3_file = "s3://rackspace-image-archive/test.txt"

    service, file = s3_file.split(":")
    assert service == "s3"

    success = fc._put_to_aws(file, "test")
    assert success


def test_get_from_aws():
    config.update_from_file('settings.py')
    fc = FileCopier()

    s3_file = "s3://rackspace-image-archive/test.txt"

    service, file = s3_file.split(":")
    assert service == "s3"

    body = fc._get_from_aws(file)

    assert body == b"test"
