"""shaarli-client main CLI entrypoint"""
import json
import sys
from argparse import ArgumentParser

from .client import ShaarliV1Client
from .utils import generate_all_endpoints_parsers


def main():
    """Main CLI entrypoint"""
    parser = ArgumentParser()
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
        '--output',
        choices=['json', 'pprint', 'text'],
        default='json',
        help="Output formatting"
    )

    subparsers = parser.add_subparsers(
        dest='endpoint_name',
        help="REST API endpoint"
    )

    generate_all_endpoints_parsers(subparsers, ShaarliV1Client.endpoints)

    args = parser.parse_args()

    try:
        response = ShaarliV1Client(args.url, args.secret).request(args)
        print(response.url)
    except KeyError:
        parser.print_help()
        sys.exit(1)

    if args.output == 'json':
        print(response.json())
    elif args.output == 'pprint':
        print(json.dumps(response.json(), sort_keys=True, indent=4))
    elif args.output == 'text':
        print(response.text)
