"""shaarli-client main CLI entrypoint"""
import logging
import sys
from argparse import ArgumentParser

from .client import ShaarliV1Client
from .config import InvalidConfiguration, get_credentials
from .utils import format_response, generate_all_endpoints_parsers, write_output


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
        '-f',
        '--format',
        choices=['json', 'pprint', 'text'],
        default='pprint',
        help="Output formatting"
    )
    parser.add_argument(
        '-o',
        '--outfile',
        help="File to save the program output to"
    )
    parser.add_argument(
        '--insecure',
        action='store_true',
        help="Bypass API SSL/TLS certificate verification"
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
        parser.print_help()
        sys.exit(1)
    except (KeyError, TypeError, ValueError) as exc:
        logging.error(exc)
        parser.print_help()
        sys.exit(1)

    output = format_response(args.format, response)
    if not args.outfile:
        print(output)
    else:
        write_output(args.outfile, output)
