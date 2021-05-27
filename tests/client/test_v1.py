"""Tests for Shaarli REST API v1 client"""
# pylint: disable=invalid-name,protected-access
from argparse import ArgumentTypeError, Namespace
from unittest import mock

import pytest
from requests.exceptions import InvalidSchema, InvalidURL, MissingSchema

from shaarli_client.client.v1 import (InvalidEndpointParameters,
                                      ShaarliV1Client, check_positive_integer)

SHAARLI_URL = 'http://domain.tld/shaarli'
SHAARLI_SECRET = 's3kr37!'


def test_check_positive_integer():
    """A posivite integer is a positive integer"""
    assert check_positive_integer('0') == 0
    assert check_positive_integer('2378') == 2378


def test_check_positive_integer_negative():
    """A negative integer is not a positive integer"""
    with pytest.raises(ArgumentTypeError) as exc:
        check_positive_integer('-123')
    assert 'not a positive integer' in str(exc.value)


def test_check_positive_integer_alpha():
    """An alphanumeric string is not a positive integer"""
    with pytest.raises(ArgumentTypeError) as exc:
        check_positive_integer('abc123')
    assert 'not a positive integer' in str(exc.value)


def test_invalid_endpoint_parameters_exception():
    """Custom exception formatting"""
    exc = InvalidEndpointParameters('post-dummy', ['param1', 'param2'])
    assert str(exc) == \
        "Invalid parameters for endpoint 'post-dummy': param1, param2"


def test_constructor():
    """Instantiate a new client"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET)


def test_constructor_no_uri():
    """Missing URI"""
    with pytest.raises(TypeError) as exc:
        ShaarliV1Client(None, SHAARLI_SECRET)
    assert "Missing Shaarli URI" in str(exc.value)


def test_constructor_no_secret():
    """Missing authentication secret"""
    with pytest.raises(TypeError) as exc:
        ShaarliV1Client(SHAARLI_URL, None)
    assert "Missing Shaarli secret" in str(exc.value)


@pytest.mark.parametrize("test_uri", [
    SHAARLI_URL,
    '%s/' % SHAARLI_URL,
    '%s///' % SHAARLI_URL,
])
def test_constructor_strip_uri(test_uri):
    """Ensure trailing / are stripped"""
    client = ShaarliV1Client(test_uri, SHAARLI_SECRET)
    assert client.uri == SHAARLI_URL


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
        headers=mock.ANY,
        verify=True,
        params={}
    )


@pytest.mark.parametrize('uri, klass, msg', [
    ('shaarli', MissingSchema, "No schema supplied"),
    ('http:/shaarli', InvalidURL, "No host supplied"),
    ('htp://shaarli', InvalidSchema, "No connection adapters"),
])
def test_get_info_invalid_uri(uri, klass, msg):
    """Invalid URI format"""
    with pytest.raises(ValueError) as exc:
        ShaarliV1Client(uri, SHAARLI_SECRET).get_info()
    assert isinstance(exc.value, klass)
    assert msg in str(exc.value)


@mock.patch('requests.request')
def test_get_links_uri(request):
    """Ensure the proper endpoint URI is accessed"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET).get_links({})
    request.assert_called_once_with(
        'GET',
        '%s/api/v1/links' % SHAARLI_URL,
        headers=mock.ANY,
        verify=True,
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


@mock.patch('requests.request')
def test_post_links_uri(request):
    """Ensure the proper endpoint URI is accessed"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET).post_link({})
    request.assert_called_once_with(
        'POST',
        '%s/api/v1/links' % SHAARLI_URL,
        headers=mock.ANY,
        verify=True,
        json={}
    )


def test_retrieve_http_params_post_link():
    """Retrieve REST parameters from an Argparse Namespace - POST /links"""
    args = Namespace(
        endpoint_name='post-link',
        description="I am not a bookmark about a link.",
        private=False,
        tags=["nope", "4891"],
        title="Ain't Talkin' 'bout Links",
        url='https://aint.talkin.bout.lin.ks'
    )
    assert ShaarliV1Client._retrieve_http_params(args) == \
        (
            'POST',
            'links',
            {
                'description': "I am not a bookmark about a link.",
                'private': False,
                'tags': ["nope", "4891"],
                'title': "Ain't Talkin' 'bout Links",
                'url': 'https://aint.talkin.bout.lin.ks'
            }
        )


def test_retrieve_http_params_post_empty_link():
    """Retrieve REST parameters from an Argparse Namespace - POST /links"""
    args = Namespace(endpoint_name='post-link')
    assert ShaarliV1Client._retrieve_http_params(args) == ('POST', 'links', {})


@mock.patch('requests.request')
def test_put_links_uri(request):
    """Ensure the proper endpoint URI is accessed"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET).put_link(12, {})
    request.assert_called_once_with(
        'PUT',
        '%s/api/v1/links/12' % SHAARLI_URL,
        headers=mock.ANY,
        verify=True,
        json={}
    )


def test_retrieve_http_params_put_link():
    """Retrieve REST parameters from an Argparse Namespace - PUT /links"""
    args = Namespace(
        resource=46,
        endpoint_name='put-link',
        description="I am not a bookmark about a link.",
        private=False,
        tags=["nope", "4891"],
        title="Ain't Talkin' 'bout Links",
        url='https://aint.talkin.bout.lin.ks'
    )
    assert ShaarliV1Client._retrieve_http_params(args) == \
        (
            'PUT',
            'links/46',
            {
                'description': "I am not a bookmark about a link.",
                'private': False,
                'tags': ["nope", "4891"],
                'title': "Ain't Talkin' 'bout Links",
                'url': 'https://aint.talkin.bout.lin.ks'
            }
        )


def test_retrieve_http_params_put_empty_link():
    """Retrieve REST parameters from an Argparse Namespace - PUT /links"""
    args = Namespace(
        resource=485,
        endpoint_name='put-link'
    )
    assert ShaarliV1Client._retrieve_http_params(args) == \
        ('PUT', 'links/485', {})


def test_retrieve_http_params_get_tags():
    """Retrieve REST parameters from an Argparse Namespace - GET /tags"""
    args = Namespace(
        endpoint_name='get-tags',
        offset=42,
        limit='all',
        visibility='public'
    )
    assert ShaarliV1Client._retrieve_http_params(args) == \
        ('GET', 'tags', {'offset': 42, 'limit': 'all', 'visibility': 'public'})


@mock.patch('requests.request')
def test_get_tags_uri(request):
    """Ensure the proper endpoint URI is accessed"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET).get_tags({})
    request.assert_called_once_with(
        'GET',
        '%s/api/v1/tags' % SHAARLI_URL,
        headers=mock.ANY,
        verify=True,
        params={}
    )


@mock.patch('requests.request')
def test_put_tags_uri(request):
    """Ensure the proper endpoint URI is accessed"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET).put_tag('some-tag', {})
    request.assert_called_once_with(
        'PUT',
        '%s/api/v1/tags/some-tag' % SHAARLI_URL,
        headers=mock.ANY,
        verify=True,
        json={}
    )


def test_retrieve_http_params_put_tag():
    """Retrieve REST parameters from an Argparse Namespace - PUT /tags"""
    args = Namespace(
        resource='some-tag',
        endpoint_name='put-tag',
        name='new-tag',
    )
    assert ShaarliV1Client._retrieve_http_params(args) == \
        (
            'PUT',
            'tags/some-tag',
            {
                'name': 'new-tag',
            }
        )


def test_retrieve_http_params_put_empty_tag():
    """Retrieve REST parameters from an Argparse Namespace - PUT /tags"""
    args = Namespace(
        resource='some-tag',
        endpoint_name='put-tag'
    )
    assert ShaarliV1Client._retrieve_http_params(args) == \
        ('PUT', 'tags/some-tag', {})


@mock.patch('requests.request')
def test_delete_tags_uri(request):
    """Ensure the proper endpoint URI is accessed"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET).delete_tag('some-tag', {})
    request.assert_called_once_with(
        'DELETE',
        '%s/api/v1/tags/some-tag' % SHAARLI_URL,
        headers=mock.ANY,
        verify=True,
        json={}
    )


@mock.patch('requests.request')
def test_delete_link_uri(request):
    """Ensure the proper endpoint URI is accessed"""
    ShaarliV1Client(SHAARLI_URL, SHAARLI_SECRET).delete_link(1234, {})
    request.assert_called_once_with(
        'DELETE',
        '%s/api/v1/links/1234' % SHAARLI_URL,
        headers=mock.ANY,
        verify=True,
        json={}
    )


def test_retrieve_http_params_delete_tag():
    """Retrieve REST parameters from an Argparse Namespace - DELETE /tags"""
    args = Namespace(
        resource='some-tag',
        endpoint_name='delete-tag',
    )
    assert ShaarliV1Client._retrieve_http_params(args) == \
        (
            'DELETE',
            'tags/some-tag',
            {}
        )


def test_retrieve_http_params_delete_empty_tag():
    """Retrieve REST parameters from an Argparse Namespace - DELETE /tags"""
    args = Namespace(
        resource='some-tag',
        endpoint_name='delete-tag'
    )
    assert ShaarliV1Client._retrieve_http_params(args) == \
        ('DELETE', 'tags/some-tag', {})
