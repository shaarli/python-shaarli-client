"""Shaarli REST API v1 client"""
import calendar
import time
from argparse import Action

import requests
from requests_jwt import JWTAuth


class SearchFormatAction(Action):
    """Format values for searching"""

    # pylint: disable=too-few-public-methods

    def __call__(self, parser, namespace, values, option_string=None):
        """Convert a list of strings to a search query string

        Source:           ["term1", "term2", "term3", ...]
        Formatted string: "term1 term2 term3 ..."

        Actual query:     term1+term2+term3+...
        """
        setattr(namespace, self.dest, ' '.join(values))


class InvalidEndpointParameters(Exception):
    """Raised when unauthorized endpoint parameters are used"""

    def __init__(self, endpoint_name, parameters):
        """Custom exception message"""
        super(InvalidEndpointParameters, self).__init__(
            "Invalid parameters for endpoint '%s': %s" % (
                endpoint_name,
                ", ".join(parameters)
            )
        )


class ShaarliV1Client:
    """Shaarli REST API v1 client"""

    endpoints = {
        'get-info': {
            'path': 'info',
            'method': 'GET',
            'help': "Get information about this instance",
            'params': None,
        },
        'get-links': {
            'path': 'links',
            'method': 'GET',
            'help': "Get a collection of links ordered by creation date",
            'params': {
                'offset': {
                    'help': "Offset from which to start listing links",
                    'type': int,
                },
                'limit': {
                    'help': "Number of links to retrieve or 'all'",
                },
                'searchtags': {
                    'help': "List of tags",
                    'nargs': '+',
                    'action': SearchFormatAction,
                },
                'searchterm': {
                    'help': "Search terms across all links fields",
                    'nargs': '+',
                    'action': SearchFormatAction,
                },
                'visibility': {
                    'choices': ['all', 'private', 'public'],
                    'help': "Filter links by visibility",
                },
            },
        },
    }

    def __init__(self, uri, secret):
        """Client constructor"""
        self.uri = uri
        self.secret = secret
        self.version = 1

    @classmethod
    def _check_endpoint_params(cls, endpoint_name, params):
        """Check parameters are allowed for a given endpoint"""
        if not params:
            return

        invalid_parameters = list()

        for param in params.keys():
            if param not in cls.endpoints[endpoint_name]['params'].keys():
                invalid_parameters.append(param)

        if invalid_parameters:
            raise InvalidEndpointParameters(endpoint_name, invalid_parameters)

    @classmethod
    def _retrieve_http_params(cls, args):
        """Retrieve REST HTTP parameters from an Argparse Namespace

        This is done by introspecing the parsed arguments with reference to
        the client's endpoint metadata.
        """
        endpoint = cls.endpoints[args.endpoint_name]

        if not endpoint.get('params'):
            return (endpoint['method'], endpoint['path'], {})

        params = {
            param: getattr(args, param)
            for param in endpoint.get('params').keys()
            if hasattr(args, param)
        }

        return (endpoint['method'], endpoint['path'], params)

    def _request(self, method, endpoint, params):
        """Send an HTTP request to this instance"""
        auth = JWTAuth(self.secret, alg='HS512', header_format='Bearer %s')
        auth.add_field('iat', lambda req: calendar.timegm(time.gmtime()))

        endpoint_uri = '%s/api/v%d/%s' % (self.uri, self.version, endpoint)
        return requests.request(method, endpoint_uri, auth=auth, params=params)

    def request(self, args):
        """Send a parameterized request to this instance"""
        return self._request(* self._retrieve_http_params(args))

    def get_info(self):
        """Get information about this instance"""
        return self._request('GET', 'info', {})

    def get_links(self, params):
        """Get a collection of links ordered by creation date"""
        self._check_endpoint_params('get-links', params)
        return self._request('GET', 'links', params)
