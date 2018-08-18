import logging
from logging.config import dictConfig
from os import environ, path


def setup_logging():
    """Setup logging."""
    runs_on_lambda = environ.get('AWS_LAMBDA', False)

    if runs_on_lambda == "True":
        logging_config = dict(
            version=1,
            formatters={
                'format': {
                    'format':
                    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
                }
            },
            handlers={
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'format',
                    'level': logging.DEBUG
                }
            },
            root={
                'handlers': ['console'],
                'level': logging.DEBUG,
            },
        )
    else:
        file_name = "migrate.log"

        stage = environ.get('STAGE', 'development')
        production_log_file = "/var/log/%s" % file_name
        if stage == 'production' and path.isfile(production_log_file):
            file_name = production_log_file

        logging_config = dict(
            version=1,
            formatters={
                'format': {
                    'format':
                    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
                }
            },
            handlers={
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'format',
                    'level': logging.DEBUG
                },
                'file': {
                    'class': 'logging.FileHandler',
                    'formatter': 'format',
                    'level': logging.DEBUG,
                    "filename": file_name,

                }
            },
            root={
                'handlers': ['console', 'file'],
                'level': logging.DEBUG,
            },
        )

    dictConfig(logging_config)

    logger = logging.getLogger()
    logger.debug('logging setup')

    return
