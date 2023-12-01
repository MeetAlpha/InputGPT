import configparser
import json

def load_config(file_name='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_name)

    attributes = dict(config['default'])
    # The temperature is a float, not str.
    attributes['temperature'] = float(attributes['temperature'])
    print(attributes)
    return attributes

def load_rules(file_name='rules.json'):
    with open(file_name, 'r') as file:
        json_data = json.load(file)
    return json_data
