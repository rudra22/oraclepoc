import oracledb
import os
import sys
import json
import yaml


class OracleOperator:
    def __init__(self, config):
        self.connection = None
        config_file = os.path.join(".", config)
        with open(config_file) as data:
            if config_file.lower().endswith('yaml') or config_file.lower().endswith('yml'):
                self.config = yaml.load(data, Loader=yaml.SafeLoader)
            elif config_file.lower().endswith('json'):
                self.config = json.load(data)
            else:
                print("Unknown configuration file type!")
                raise Exception("Unknown configuration file type!")
        print(self.config)

        env = os.environ.get('db_env', 'dev')
        try:
            self.user = self.config['connection']['db']['name'][env]['user_name']
            self.password = self.config['connection']['db']['name'][env]['password']
            self.connection_string = self.config['connection']['db']['name'][env]['connect_string']
        except Exception as e:
            raise Exception("Not all connection info available. {}".format(repr(e)))
        self.get_conn()

    def get_conn(self):
        if not self.connection:
            self.connection = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=self.connection_string)
            print("Successfully connected to {} with {}".format(self.user, self.connection_string))
        return self.connection

    def get_cursor(self):
        return self.connection.cursor()
