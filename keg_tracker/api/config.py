import json
from ast import literal_eval


class ConfigDict(object):

    def __init__(self):
        self.conf_dict = {}
        self.config_dict()

    def config_dict(self) -> dict:
        c_response = self.config_file_locator(file_location='../')
        if c_response[1] is False:
            c_response = self.config_file_locator(file_location='../../')
        if c_response[1] is True:
            self.conf_dict = json.loads(c_response[0])
        else:
            self.conf_dict = {'error': 'Unable to open config.json'}

    def config_file_locator(self, file_location='') -> str:
        try:
            with open(f'{file_location}/config.json', mode='r') as c_file:
                config_file = c_file.read()
        except FileNotFoundError:
            return 'File not found.', False
        return config_file, True


conf_dict = ConfigDict().conf_dict
LOG_LEVEL = conf_dict['logging_level']
FLASK_DEBUG = False
THREADED = True
USE_SSL = literal_eval(conf_dict['ssl'])
BASE_URL = False
PROCESSES = 1

if '__main__' == __name__:
    cd = ConfigDict()
    print(type(cd.conf_dict))