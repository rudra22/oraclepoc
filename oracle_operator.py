import oracledb
from utils import safe_get
# from vault_config import VaultManager


class OracleOperator:
    def __init__(self, config_file):
        # secrets = VaultManager(config_file).get_secrets()
        self.connection = None
        # self.user = safe_get(secrets, 'user_name')
        # self.password = safe_get(secrets, 'password')
        # self.connection_string = safe_get(secrets, 'dsn')
        self.user = "rghosh"
        self.password = "rghosh"
        self.connection_string = "localhost:1521/?service_name=xepdb1"
        self.get_conn()

    def get_db_uri(self):
        return 'oracle+oracledb://' + self.user + ":" + self.password + "@" + self.connection_string

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
