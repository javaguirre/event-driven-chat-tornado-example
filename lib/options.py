import yaml


def get_options():
    data = {}

    with open('../options.yml', 'r') as f:
        data = yaml.load(f)

    return data
