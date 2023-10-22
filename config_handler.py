import configparser

def load_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)

    attributes = dict(config['default'])
    # The temperature is a float, not str.
    attributes['temperature'] = float(attributes['temperature'])
    print(attributes)
    return attributes
