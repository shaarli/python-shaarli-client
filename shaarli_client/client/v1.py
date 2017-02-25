"""Shaarli REST API v1 client"""
import calendar
import time

import requests
from requests_jwt import JWTAuth


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
