"""shaarli-client main CLI entrypoint"""
import json
import logging
import sys
from argparse import ArgumentParser

from .client import ShaarliV1Client
from .config import InvalidConfiguration, get_credentials
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
    except InvalidConfiguration as exc:
        logging.error(exc)
        sys.exit(1)
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
