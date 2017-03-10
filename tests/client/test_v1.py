"""Tests for Shaarli REST API v1 client"""
# pylint: disable=invalid-name,protected-access
from argparse import Namespace
from unittest import mock

import pytest

from shaarli_client.client import InvalidEndpointParameters, ShaarliV1Client

SHAARLI_URL = 'http://domain.tld/shaarli/'
SHAARLI_SECRET = 's3kr37!'


def test_invalid_endpoint_parameters_exception():
    """Custom exception formatting"""
    exc = InvalidEndpointParameters('post-dummy', ['param1', 'param2'])
    assert str(exc) == \
        "Invalid parameters for endpoint 'post-dummy': param1, param2"


def test_constructor():
    """Instantiate a new client"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET)


def test_check_endpoint_params_none():
    """Check parameters - none passed"""
    ShaarliV1Client._check_endpoint_params('get-info', None)


def test_check_endpoint_params_empty():
    """Check parameters - empty dict passed"""
    ShaarliV1Client._check_endpoint_params('get-info', {})


def test_check_endpoint_params_ok():
    """Check parameters - valid params passed"""
    ShaarliV1Client._check_endpoint_params(
        'get-links',
        {'offset': 3, 'limit': 100}
    )


def test_check_endpoint_params_nok():
    """Check parameters - invalid params passed"""
    with pytest.raises(InvalidEndpointParameters) as exc:
        ShaarliV1Client._check_endpoint_params(
            'get-links',
            {'get': 27, 'forget': 31}
        )
    assert "'get-links':" in str(exc.value)
    assert 'get' in str(exc.value)
    assert 'forget' in str(exc.value)


def test_check_endpoint_params_nok_mixed():
    """Check parameters - valid & invalid params passed"""
    with pytest.raises(InvalidEndpointParameters) as exc:
        ShaarliV1Client._check_endpoint_params(
            'get-links',
            {'offset': 200, 'preset': 27, 'headset': 31}
        )
    assert "'get-links':" in str(exc.value)
    assert 'headset' in str(exc.value)
    assert 'preset' in str(exc.value)


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


@mock.patch('requests.request')
def test_get_links_uri(request):
    """Ensure the proper endpoint URI is accessed"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET).get_links({})
    request.assert_called_once_with(
        'GET',
        '%s/api/v1/links' % SHAARLI_URL,
        auth=mock.ANY,
        params={}
    )


def test_retrieve_http_params_get_info():
    """Retrieve REST parameters from an Argparse Namespace - GET /info"""
    args = Namespace(endpoint_name='get-info')
    assert ShaarliV1Client._retrieve_http_params(args) == \
        ('GET', 'info', {})


def test_retrieve_http_params_get_links():
    """Retrieve REST parameters from an Argparse Namespace - GET /links"""
    args = Namespace(
        endpoint_name='get-links',
        offset=42,
        limit='all',
        visibility='public'
    )
    assert ShaarliV1Client._retrieve_http_params(args) == \
        ('GET', 'links', {'offset': 42, 'limit': 'all', 'visibility': 'public'})


def test_retrieve_http_params_get_links_searchterm():
    """Retrieve REST parameters from an Argparse Namespace - GET /links"""
    args = Namespace(
        endpoint_name='get-links',
        searchterm='gimme+some+results'
    )
    assert ShaarliV1Client._retrieve_http_params(args) == \
        ('GET', 'links', {'searchterm': 'gimme+some+results'})
