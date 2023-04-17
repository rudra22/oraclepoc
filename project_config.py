import json
import os
import yaml
from utils import file_type


class ConfigManager:
    def __init__(self, project_config_file='../config/project_config.yaml',
                 log_config_file='../config/log_config.yaml'):
        self.cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_config_file = os.path.join(self.cur_dir, project_config_file)
        self.log_config_file = os.path.join(self.cur_dir, log_config_file)
        self.project_config = None
        self.log_config = None

    def get_project_config(self):
        if os.path.exists(self.project_config_file):
            f_type = file_type(self.project_config_file)
            with open(self.project_config_file) as f:
                if f_type.__eq__('yml'):
                    self.project_config = yaml.safe_load(f)
                elif f_type.__eq__('json'):
                    self.project_config = json.load(f)
                else:
                    raise Exception("Unknown project configuration file type!")
        return self.project_config

    def put_project_config(self, data):
        if os.path.exists(self.project_config_file):
            f_type = file_type(self.project_config_file)
            with open(self.project_config_file, "w") as f:
                if f_type.__eq__('yml'):
                    yaml.dump(data, f)
                elif f_type.__eq__('json'):
                    json.dump(data, f)
        return self.get_project_config()

    def get_log_config(self):
        if os.path.exists(self.log_config_file):
            f_type = file_type(self.log_config_file)
            with open(self.log_config_file) as f:
                if f_type.__eq__('yml'):
                    self.log_config = yaml.safe_load(f)
                elif f_type.__eq__('json'):
                    self.log_config = json.load(f)
                else:
                    raise Exception("Unknown log configuration file type!")
        return self.log_config
