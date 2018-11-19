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

    assert config.secret(key) == 'FINDME'
