"""Configuration file utilities"""
import logging
import os
from configparser import ConfigParser
from pathlib import Path


class InvalidConfiguration(Exception):
    """Raised when invalid/no configuration is found"""

    def __init__(self, message):
        """Custom exception message"""
        super(InvalidConfiguration, self).__init__(
            "Invalid configuration: %s" % message
        )


def get_credentials(args):
    """Retrieve Shaarli authentication information"""
    if args.url and args.secret:
        # credentials passed as CLI arguments
        logging.warning("Passing credentials as arguments is unsafe"
                        " and should be used for debugging only")
        return (args.url, args.secret)

    config = ConfigParser()

    if args.instance:
        instance = 'shaarli:{}'.format(args.instance)
    else:
        instance = 'shaarli'

    if args.config:
        # user-specified configuration file
        config_files = config.read([args.config])
    else:
        # load configuration from a list of possible locations
        home = Path(os.path.expanduser('~'))
        config_files = config.read([
            str(home / '.config' / 'shaarli' / 'client.ini'),
            str(home / '.shaarli_client.ini'),
            'shaarli_client.ini'
        ])

    if not config_files:
        raise InvalidConfiguration("No configuration file found")

    logging.info("Reading configuration from: %s",
                 ', '.join([str(cfg) for cfg in config_files]))

    try:
        return (config[instance]['url'], config[instance]['secret'])
    except KeyError as exc:
        raise InvalidConfiguration("Missing entry: %s" % exc)
