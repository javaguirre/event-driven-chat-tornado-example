import yaml

from lib.backend import RedisBackend, RedisMobileBackend


def get_options():
    data = {}

    with open('options.yml', 'r') as f:
        data = yaml.load(f)

    # TODO We could get redis or other backend data
    # from the yml file
    data['backend'] = RedisBackend()
    data['mobile_backend'] = RedisMobileBackend()

    return data
