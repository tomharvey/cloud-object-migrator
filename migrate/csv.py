from csv import DictReader


def read_csv(csv_path):
    """Read a CSV and yield each row as a Dict."""
    with open(csv_path, newline='') as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            yield row


def get_message_from_row(row):
    """Split the row into a message and any extras."""
    message = {}
    for message_key in ['source', 'destination']:
        message[message_key] = row.pop(message_key)
    extras = row if len(row) > 0 else None
    return message, extras
