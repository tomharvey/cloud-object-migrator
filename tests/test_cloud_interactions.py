from migrate.copy import FileCopier
from migrate.config import config


def test_get_from_rackspace():
    config.update_from_file('settings.py')
    FC = FileCopier()

    cloudfile = "cloudfiles://important_things/test.txt"
    service, file = cloudfile.split(":")

    assert service == "cloudfiles"

    headers, body = FC._get_source_from_rackspace(file)

    assert headers['etag'] == "098f6bcd4621d373cade4e832627b4f6"
    assert body == "test"
