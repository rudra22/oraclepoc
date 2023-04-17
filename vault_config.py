import os
import hvac
from project_config import ConfigManager
from utils import coalesce, safe_get


class VaultManager:
    def __init__(self, config_file, vault_path=None, vault_token=None):
        self.env = os.environ.get('env') if os.environ.get('env', None) else 'Dev'
        self.config_data = safe_get(ConfigManager(config_file).get_project_config(), self.env)

        self.cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.cert_file = os.path.join(self.cur_dir, safe_get(self.config_data, 'cert_file'))

        vault_data = safe_get(self.config_data, 'vault')
        self.secrets = None
        self.client = None

        self._fetch_secrets(vault_data, vault_path, vault_token)

    def _fetch_secrets(self, vault_data, vault_path, vault_token):
        url = safe_get(vault_data, 'vault_uri')
        token = coalesce(vault_token, os.environ.get('vault_token', None), safe_get(vault_data, 'vault_token'))
        self.client = hvac.Client(url=url, token=token, verify=self.cert_file)
        vault_path = coalesce(vault_path, os.environ.get('vault_path'), safe_get(vault_data, 'vault_path'))
        if self.client.is_authenticated():
            self.secrets = self.client.read(path=vault_path)
        else:
            raise Exception("Invalid Hashicorp Vault Token Specified")

    def get_secrets(self):
        return self.secrets
