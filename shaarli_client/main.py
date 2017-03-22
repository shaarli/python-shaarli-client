"""shaarli-client main CLI entrypoint"""
import json
import logging
import os
import sys
from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path

from .client import ShaarliV1Client
from .utils import generate_all_endpoints_parsers


def main():
    """Main CLI entrypoint"""
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help="Configuration file"
    )
    parser.add_argument(
        '-i',
        '--instance',
        help="Shaarli instance (configuration alias)"
    )
    parser.add_argument(
        '-u',
        '--url',
        help="Shaarli instance URL"
    )
    parser.add_argument(
        '-s',
        '--secret',
        help="API secret"
    )
    parser.add_argument(
        '--format',
        choices=['json', 'pprint', 'text'],
        default='pprint',
        help="Output formatting"
    )

    subparsers = parser.add_subparsers(
        dest='endpoint_name',
        help="REST API endpoint"
    )

    generate_all_endpoints_parsers(subparsers, ShaarliV1Client.endpoints)

    args = parser.parse_args()

    try:
        url, secret = get_credentials(args)
        response = ShaarliV1Client(url, secret).request(args)

    except (KeyError, TypeError, ValueError) as exc:
        logging.error(exc)
        parser.print_help()
        sys.exit(1)

    if args.format == 'json':
        print(response.json())
    elif args.format == 'pprint':
        print(json.dumps(response.json(), sort_keys=True, indent=4))
    elif args.format == 'text':
        print(response.text)


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
        logging.info("Reading configuration from: %s", args.config)
        with open(args.config, 'r') as f_config:
            config.read_file(f_config)
    else:
        # load configuration from a list of possible locations
        home = Path(os.path.expanduser('~'))
        config_files = config.read([
            home / '.config' / 'shaarli' / 'client.ini',
            home / '.shaarli_client.ini',
            'shaarli_client.ini'
        ])
        logging.info("Reading configuration from: %s",
                     ', '.join([str(cfg) for cfg in config_files]))

    return (config[instance]['url'], config[instance]['secret'])
