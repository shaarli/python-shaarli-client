"""Tests for Shaarli REST API v1 client"""
# pylint: disable=invalid-name,protected-access
from unittest import mock

from shaarli_client.client import ShaarliV1Client

SHAARLI_URL = 'http://domain.tld/shaarli/'
SHAARLI_SECRET = 's3kr37!'


def test_constructor():
    """Instantiate a new client"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET)


@mock.patch('requests.request')
def test_get_info_uri(request):
    """Ensure the proper endpoint URI is accessed"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET).get_info()
    request.assert_called_once_with(
        'GET',
        '%s/api/v1/info' % SHAARLI_URL,
        auth=mock.ANY,
        params={}
    )
