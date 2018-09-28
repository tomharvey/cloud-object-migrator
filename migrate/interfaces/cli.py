import click

from migrate.config import config
from migrate.copy import FileCopier
from migrate.csv import get_message_from_row, read_csv
from migrate.logging import setup_logging
from migrate.sqs import Sqs


@click.group()
@click.option('--config', 'config_file', help='Path to config file.')
def cli(config_file):
    """Load the config.

    When running a local command you should specify a settings file which
    should contain details of the environment.
    """
    if config_file is not None:
        config.update_from_file(config_file)


@cli.command()
@click.option('--csv', 'csv_path', help='Path to a CSV file.')
def from_csv(csv_path):
    """Add data from a csv file."""
    setup_logging()
    sqs = Sqs()

    for row in read_csv(csv_path):
        message, extras = get_message_from_row(row)
        sqs.add_message(message, extras)


@cli.command()
def consume_queue():
    """Locally consume the queue."""
    setup_logging()
    sqs = Sqs()

    sqs.consume_queue()


@cli.command()
@click.option('--source', 'source', help='source.')
@click.option('--destination', 'destination', help='destination.')
def copy(source, destination):
    """Copy one file."""
    fc = FileCopier()

    source_content = fc.get_source(source)
    success = fc.put_destination(destination, source_content)
    return success
