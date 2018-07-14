"""Tests for Shaarli client utilities"""
# pylint: disable=invalid-name
import json
from argparse import ArgumentParser
from unittest import mock

import pytest
from requests import Response

from shaarli_client.utils import format_response, generate_endpoint_parser


@mock.patch('argparse.ArgumentParser.add_argument')
def test_generate_endpoint_parser_noparam(addargument):
    """Generate a parser from endpoint metadata - no params"""
    name = 'put-stuff'
    metadata = {
        'path': 'stuff',
        'method': 'PUT',
        'help': "Changes stuff",
        'params': {},
    }
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    generate_endpoint_parser(subparsers, name, metadata)

    addargument.assert_has_calls([
        # first helper for the main parser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # second helper for the 'put-stuff' subparser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY)
    ])


@mock.patch('argparse.ArgumentParser.add_argument')
def test_generate_endpoint_parser_single_param(addargument):
    """Generate a parser from endpoint metadata - single param"""
    name = 'get-stuff'
    metadata = {
        'path': 'stuff',
        'method': 'GET',
        'help': "Gets stuff",
        'params': {
            'param1': {
                'help': "First param",
            },
        },
    }
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    generate_endpoint_parser(subparsers, name, metadata)

    addargument.assert_has_calls([
        # first helper for the main parser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # second helper for the 'put-stuff' subparser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # param1
        mock.call('--param1', help="First param")
    ])


@mock.patch('argparse.ArgumentParser.add_argument')
def test_generate_endpoint_parser_multi_param(addargument):
    """Generate a parser from endpoint metadata - multiple params"""
    name = 'get-stuff'
    metadata = {
        'path': 'stuff',
        'method': 'GET',
        'help': "Gets stuff",
        'params': {
            'param1': {
                'help': "First param",
                'type': int,
            },
            'param2': {
                'choices': ['a', 'b', 'c'],
                'help': "Second param",
                'nargs': '+',
            },
        },
    }
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    generate_endpoint_parser(subparsers, name, metadata)

    addargument.assert_has_calls([
        # first helper for the main parser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # second helper for the 'put-stuff' subparser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # param1
        mock.call('--param1', help="First param", type=int),

        # param2
        mock.call('--param2', choices=['a', 'b', 'c'],
                  help="Second param", nargs='+')
    ])


@mock.patch('argparse.ArgumentParser.add_argument')
def test_generate_endpoint_parser_resource(addargument):
    """Generate a parser from endpoint metadata - API resource"""
    name = 'get-stuff'
    metadata = {
        'path': 'stuff',
        'method': 'GET',
        'help': "Gets stuff",
        'resource': {
            'help': "API resource",
            'type': int,
        },
        'params': {},
    }
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    generate_endpoint_parser(subparsers, name, metadata)

    addargument.assert_has_calls([
        # first helper for the main parser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # second helper for the 'put-stuff' subparser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # resource
        mock.call('resource', help="API resource", type=int)
    ])


def test_format_response_unsupported_format():
    """Attempt to use an unsupported formatting flag"""
    response = Response()
    response.__setstate__({'_content': b'{"field":"value"}'})

    with pytest.raises(ValueError) as err:
        format_response('xml', response)

    assert "not a supported format" in str(err.value)


@pytest.mark.parametrize('output_format', ['json', 'pprint', 'text'])
def test_format_response_empty_body(output_format):
    """Format a Requests Response object with no body"""
    response = Response()
    assert format_response(output_format, response) == ''


def test_format_response_text():
    """Format a Requests Response object to plain text"""
    response = Response()
    response.__setstate__({
        '_content': b'{"global_counter":3251,'
                    b'"private_counter":1,'
                    b'"settings":{"title":"Yay!","header_link":"?",'
                    b'"timezone":"UTC",'
                    b'"enabled_plugins":["qrcode","token"],'
                    b'"default_private_links":false}}',
    })

    assert isinstance(response.text, str)
    assert response.text == '{"global_counter":3251,' \
                            '"private_counter":1,' \
                            '"settings":{"title":"Yay!","header_link":"?",' \
                            '"timezone":"UTC",' \
                            '"enabled_plugins":["qrcode","token"],' \
                            '"default_private_links":false}}'


def test_format_response_json():
    """Format a Requests Response object to JSON"""
    response = Response()
    response.__setstate__({
        '_content': b'{"global_counter":3251,'
                    b'"private_counter":1,'
                    b'"settings":{"title":"Yay!","header_link":"?",'
                    b'"timezone":"UTC",'
                    b'"enabled_plugins":["qrcode","token"],'
                    b'"default_private_links":false}}',
    })

    assert isinstance(response.json(), dict)

    # Ensure valid JSON is returned after formatting
    assert json.loads(format_response('json', response))
    assert json.loads(format_response('pprint', response))
