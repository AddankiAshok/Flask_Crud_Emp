import configparser

def read_db_params():
    config = configparser.ConfigParser()
    config.read('config/config.env')
    return config