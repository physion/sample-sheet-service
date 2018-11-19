import os
import logging


def configuration(name, default=None):
    if name in os.environ:
        return os.environ[name]

    return default


SECRETS_PATH = '/tmp/secrets/'


def secret(name, secrets_path=SECRETS_PATH, default=None):
    if name in os.environ:
        logging.debug("Found secret {} in environment variable".format(name))
        return os.environ[name]

    name = os.path.join(secrets_path, name)

    if os.path.exists(name):
        with open(name, 'r') as f:
            return f.read()

    return default
