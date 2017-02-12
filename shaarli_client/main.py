"""shaarli-client main CLI entrypoint"""
import json
from argparse import ArgumentParser

from .client import ShaarliV1Client


def main():
    """Main CLI entrypoint"""
    parser = ArgumentParser()
    parser.add_argument(
        'endpoint',
        choices=['info'],
        default='info',
        help="REST API endpoint"
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
        '--output',
        choices=['json', 'pprint', 'text'],
        default='json',
        help="Output formatting"
    )

    args = parser.parse_args()
    client = ShaarliV1Client(args.url, args.secret)

    if args.endpoint == 'info':
        response = client.info()

    if args.output == 'json':
        print(response.json())
    elif args.output == 'pprint':
        print(json.dumps(response.json(), sort_keys=True, indent=4))
    elif args.output == 'text':
        print(response.text)
