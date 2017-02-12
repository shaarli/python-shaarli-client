"""Shaarli REST API v1 client"""
import calendar
import time

import requests
from requests_jwt import JWTAuth


class ShaarliV1Client:
    """Shaarli REST API v1 client"""

    # pylint: disable=too-few-public-methods

    def __init__(self, uri, secret):
        """Client constructor"""
        self.uri = uri
        self.secret = secret
        self.version = 1

    def _request(self, method, endpoint, params):
        """Send an HTTP request to this instance"""
        auth = JWTAuth(self.secret, alg='HS512', header_format='Bearer %s')
        auth.add_field('iat', lambda req: calendar.timegm(time.gmtime()))

        endpoint_uri = '%s/api/v%d/%s' % (self.uri, self.version, endpoint)
        return requests.request(method, endpoint_uri, auth=auth, params=params)

    def info(self):
        """Get information about this instance"""
        return self._request('GET', 'info', {})
