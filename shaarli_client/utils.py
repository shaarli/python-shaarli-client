"""Utilities"""


def generate_endpoint_parser(subparsers, ep_name, ep_metadata):
    """Generate a subparser and arguments from an endpoint dictionary"""
    ep_parser = subparsers.add_parser(ep_name, help=ep_metadata['help'])

    if not ep_metadata.get('params'):
        return ep_parser

    for param, attributes in sorted(ep_metadata['params'].items()):
        ep_parser.add_argument(
            '--%s' % param,
            action=attributes.get('action'),
            choices=attributes.get('choices'),
            help=attributes.get('help'),
            nargs=attributes.get('nargs'),
            type=attributes.get('type')
        )

    return ep_parser


def generate_all_endpoints_parsers(subparsers, endpoints):
    """Generate all endpoints' subparsers from an endpoints dict"""
    for ep_name, ep_metadata in endpoints.items():
        generate_endpoint_parser(subparsers, ep_name, ep_metadata)
