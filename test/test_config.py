import svc.config as config
import os


def test_reads_secret_from_file():
    path = '/tmp/testing'
    name = 'MY_SECRET'
    secret = 'super-secret!'

    if not os.path.exists(path):
        os.mkdir(path)

    try:
        with open(os.path.join(path, name), 'w') as f:
            f.write(secret)

        assert config.secret(name, secrets_path=path) == secret

    finally:
        os.remove(os.path.join(path, name))


def test_reads_secret_from_environ():
    key = 'TEST_KEY'
    os.environ[key] = 'FINDME'

    try:
        assert config.secret(key) == 'FINDME'
    finally:
        del os.environ[key]


def test_reads_configuration_fron_environ():
    key = 'TEST_KEY'
    value = 'TEST_VALUE'
    os.environ[key] = value

    try:
        assert config.configuration(key) == value
    finally:
        del os.environ[key]


def test_allows_default_configuration():
    key = 'MISSING_KEY'
    expected = 'DEFAULT_VALUE'

    assert config.configuration(key, default=expected) == expected


def test_allows_default_secret():
    key = 'MISSING_KEY'
    expected = 'DEFAULT_VALUE'

    assert config.secret(key, default=expected) == expected
