import configparser

def load_config(filename='config.ini'):
    with open(filename, 'r') as file:
        print(file.read())
    config = configparser.ConfigParser()
    config.read(filename)
    return {
        'api_key': config.get('default', 'api_key'),
        'address': config.get('default', 'address'),
        'temperature': config.getfloat('default', 'temperature'),
        'model': config.get('default', 'model'),
        'system_role': config.get('default', 'system_role')
    }
