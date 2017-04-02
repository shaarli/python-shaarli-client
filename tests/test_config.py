"""Tests for Shaarli configuration utilities"""
# pylint: disable=invalid-name,redefined-outer-name
from argparse import Namespace
from configparser import ConfigParser

import pytest

from shaarli_client.config import InvalidConfiguration, get_credentials

SHAARLI_URL = 'http://shaar.li'
SHAARLI_SECRET = 's3kr37'


@pytest.fixture(scope='session')
def shaarli_config(tmpdir_factory):
    """Generate a client configuration file"""
    config = ConfigParser()
    config['shaarli'] = {
        'url': SHAARLI_URL,
        'secret': SHAARLI_SECRET
    }
    config['shaarli:shaaplin'] = {
        'url': SHAARLI_URL,
        'secret': SHAARLI_SECRET
    }
    config['shaarli:nourl'] = {
        'secret': SHAARLI_SECRET
    }
    config['shaarli:nosecret'] = {
        'url': SHAARLI_URL,
    }

    config_path = tmpdir_factory.mktemp('config').join('shaarli_client.ini')

    with config_path.open('w') as f_config:
        config.write(f_config)

    return config_path


def test_get_credentials_from_cli():
    """Get authentication information as CLI parameters"""
    url, secret = get_credentials(
        Namespace(url=SHAARLI_URL, secret=SHAARLI_SECRET)
    )
    assert url == SHAARLI_URL
    assert secret == SHAARLI_SECRET


@pytest.mark.parametrize('instance', [None, 'shaaplin'])
def test_get_credentials_from_config(tmpdir, shaarli_config, instance):
    """Read credentials from a standard location"""
    with tmpdir.as_cwd():
        shaarli_config.copy(tmpdir.join('shaarli_client.ini'))

        url, secret = get_credentials(
            Namespace(
                config=None,
                instance=instance,
                url=None,
                secret=None
            )
        )

    assert url == SHAARLI_URL
    assert secret == SHAARLI_SECRET


@pytest.mark.parametrize('instance', [None, 'shaaplin'])
def test_get_credentials_from_userconfig(shaarli_config, instance):
    """Read credentials from a user-provided configuration file"""
    url, secret = get_credentials(
        Namespace(
            config=str(shaarli_config),
            instance=instance,
            url=None,
            secret=None
        )
    )
    assert url == SHAARLI_URL
    assert secret == SHAARLI_SECRET


def test_get_credentials_no_config(monkeypatch):
    """No configuration file found"""
    monkeypatch.setattr(ConfigParser, 'read', lambda x, y: [])

    with pytest.raises(InvalidConfiguration) as exc:
        get_credentials(
            Namespace(
                config=None,
                instance=None,
                url=None,
                secret=None
            )
        )
    assert "No configuration file found" in str(exc.value)


def test_get_credentials_missing_section(shaarli_config):
    """The specified instance has no configuration section"""
    with pytest.raises(InvalidConfiguration) as exc:
        get_credentials(
            Namespace(
                config=str(shaarli_config),
                instance='nonexistent',
                url=None,
                secret=None
            )
        )
    assert "Missing entry: 'shaarli:nonexistent'" in str(exc.value)


@pytest.mark.parametrize('attribute', ['url', 'secret'])
def test_get_credentials_missing_attribute(shaarli_config, attribute):
    """The specified instance has no configuration section"""
    with pytest.raises(InvalidConfiguration) as exc:
        get_credentials(
            Namespace(
                config=str(shaarli_config),
                instance='no{}'.format(attribute),
                url=None,
                secret=None
            )
        )
    assert "Missing entry: '{}'".format(attribute) in str(exc.value)
