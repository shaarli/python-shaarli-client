"""Shaarli REST API v1 client"""
import calendar
import time
from argparse import Action, ArgumentTypeError

import jwt
import requests


def check_positive_integer(value):
    """Ensure a value is a positive integer"""
    try:
        intval = int(value)
    except ValueError:
        raise ArgumentTypeError("%s is not a positive integer" % value)

    if intval < 0:
        raise ArgumentTypeError("%s is not a positive integer" % value)

    return intval


class TextFormatAction(Action):
    """Format text fields"""

    # pylint: disable=too-few-public-methods

    def __call__(self, parser, namespace, values, option_string=None):
        """Convert a list of strings to a text string

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
                    'action': TextFormatAction,
                },
                'searchterm': {
                    'help': "Search terms across all links fields",
                    'nargs': '+',
                    'action': TextFormatAction,
                },
                'visibility': {
                    'choices': ['all', 'private', 'public'],
                    'help': "Filter links by visibility",
                },
            },
        },
        'post-link': {
            'path': 'links',
            'method': 'POST',
            'help': "Create a new link or note",
            'params': {
                'description': {
                    'action': TextFormatAction,
                    'help': "Link description",
                    'nargs': '+',
                },
                'private': {
                    'action': 'store_true',
                    'help': "Link visibility",
                },
                'tags': {
                    'help': "List of tags associated with the link",
                    'nargs': '+',
                },
                'title': {
                    'action': TextFormatAction,
                    'help': "Link title",
                    'nargs': '+',
                },
                'url': {
                    'help': "Link URL",
                },
            },
        },
        'put-link': {
            'path': 'links',
            'method': 'PUT',
            'help': "Update an existing link or note",
            'resource': {
                'help': "Link ID",
                'type': check_positive_integer,
            },
            'params': {
                'description': {
                    'action': TextFormatAction,
                    'help': "Link description",
                    'nargs': '+',
                },
                'private': {
                    'action': 'store_true',
                    'help': "Link visibility",
                },
                'tags': {
                    'help': "List of tags associated with the link",
                    'nargs': '+',
                },
                'title': {
                    'action': TextFormatAction,
                    'help': "Link title",
                    'nargs': '+',
                },
                'url': {
                    'help': "Link URL",
                },
            },
        },
        'get-tags': {
            'path': 'tags',
            'method': 'GET',
            'help': "Get all tags",
            'params': {
                'offset': {
                    'help': "Offset from which to start listing tags",
                    'type': int,
                },
                'limit': {
                    'help': "Number of tags to retrieve or 'all'",
                },
                'visibility': {
                    'choices': ['all', 'private', 'public'],
                },
            },
        },
        'get-tag': {
            'path': 'tags',
            'method': 'GET',
            'help': "Get a single tag",
            'resource': {
                'help': "Tag name (case-sensitive))",
            },
        },
        'put-tag': {
            'path': 'tags',
            'method': 'PUT',
            'help': "Rename an existing tag",
            'resource': {
                'help': "Tag name (case-sensitive)",
            },
            'params': {
                'name': {
                    'help': "New tag name",
                },
            },
        },
        'delete-tag': {
            'path': 'tags',
            'method': 'DELETE',
            'help': "Delete a tag from every link where it is used",
            'resource': {
                'help': "Tag name (case-sensitive)",
            },
        },
        'delete-link': {
            'path': 'links',
            'method': 'DELETE',
            'help': "Delete a link",
            'resource': {
                'help': "Link ID",
                'type': check_positive_integer,
            },
        },
    }

    def __init__(self, uri, secret):
        """Client constructor"""
        if not uri:
            raise TypeError("Missing Shaarli URI")
        if not secret:
            raise TypeError("Missing Shaarli secret")

        self.uri = uri.rstrip('/')
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

        if not endpoint.get('resource'):
            path = endpoint['path']
        else:
            path = '%s/%s' % (endpoint['path'], args.resource)

        if not endpoint.get('params'):
            return (endpoint['method'], path, {})

        params = {
            param: getattr(args, param)
            for param in endpoint.get('params').keys()
            if hasattr(args, param)
        }

        return (endpoint['method'], path, params)

    def _request(self, method, endpoint, params, verify_certs=True):
        """Send an HTTP request to this instance"""
        encoded_token = jwt.encode(
            {'iat': calendar.timegm(time.gmtime())},
            self.secret,
            algorithm='HS512',
        )
        headers = {'Authorization': 'Bearer %s' % encoded_token}

        endpoint_uri = '%s/api/v%d/%s' % (self.uri, self.version, endpoint)

        if method == 'GET':
            return requests.request(
                method,
                endpoint_uri,
                headers=headers,
                params=params,
                verify=verify_certs
            )
        return requests.request(
            method,
            endpoint_uri,
            headers=headers,
            json=params,
            verify=verify_certs
        )

    def request(self, args):
        """Send a parameterized request to this instance"""
        verify_certs = False if args.insecure else True
        return self._request(* self._retrieve_http_params(args),
                             verify_certs)

    def get_info(self):
        """Get information about this instance"""
        return self._request('GET', 'info', {})

    def get_links(self, params):
        """Get a collection of links ordered by creation date"""
        self._check_endpoint_params('get-links', params)
        return self._request('GET', 'links', params)

    def post_link(self, params):
        """Create a new link or note"""
        self._check_endpoint_params('post-link', params)
        return self._request('POST', 'links', params)

    def put_link(self, resource, params):
        """Update an existing link or note"""
        self._check_endpoint_params('put-link', params)
        return self._request('PUT', 'links/%d' % resource, params)

    def get_tags(self, params):
        """Get a list of all tags"""
        self._check_endpoint_params('get-tags', params)
        return self._request('GET', 'tags', params)

    def get_tag(self, resource, params):
        """Get a single tag"""
        self._check_endpoint_params('get-tag', params)
        return self._request('GET', 'tags/%s' % resource, params)

    def put_tag(self, resource, params):
        """Rename an existing tag"""
        self._check_endpoint_params('put-tag', params)
        return self._request('PUT', 'tags/%s' % resource, params)

    def delete_tag(self, resource, params):
        """Delete a tag"""
        self._check_endpoint_params('delete-tag', params)
        return self._request('DELETE', 'tags/%s' % resource, params)

    def delete_link(self, resource, params):
        """Delete a link"""
        self._check_endpoint_params('delete-link', params)
        return self._request('DELETE', 'links/%d' % resource, params)
