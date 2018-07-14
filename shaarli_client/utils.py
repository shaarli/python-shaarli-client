"""Utilities"""
import json


def generate_endpoint_parser(subparsers, ep_name, ep_metadata):
    """Generate a subparser and arguments from an endpoint dictionary"""
    ep_parser = subparsers.add_parser(ep_name, help=ep_metadata['help'])

    if ep_metadata.get('resource'):
        ep_parser.add_argument('resource', **ep_metadata.get('resource'))

    if not ep_metadata.get('params'):
        return ep_parser

    for param, attributes in sorted(ep_metadata['params'].items()):
        ep_parser.add_argument('--%s' % param, **attributes)

    return ep_parser


def generate_all_endpoints_parsers(subparsers, endpoints):
    """Generate all endpoints' subparsers from an endpoints dict"""
    for ep_name, ep_metadata in endpoints.items():
        generate_endpoint_parser(subparsers, ep_name, ep_metadata)


def format_response(output_format, response):
    """Format the API response to the desired output format"""
    if not response.content:
        formatted = ''
    elif output_format == 'json':
        formatted = json.dumps(response.json())
    elif output_format == 'pprint':
        formatted = json.dumps(response.json(), sort_keys=True, indent=4)
    elif output_format == 'text':
        formatted = response.text
    else:
        raise ValueError("%s is not a supported format." % output_format)

    return formatted


def write_output(filename, output):
    """Write the program output to a file"""
    try:
        with open(filename, 'w') as outfile_handler:
            outfile_handler.write(output)
    except OSError:
        raise OSError("Unable to write output file %s" % filename)
