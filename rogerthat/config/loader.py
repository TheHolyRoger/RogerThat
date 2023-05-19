# Private config vars
import sys

from rogerthat.config.utils import config_utils


class config_loader:
    def __init__(self, *args, **kwargs):
        self._app_config = None
        self._db_config = None
        self._mqtt_config = None
        self._tv_config = None
        self._web_config = None
        self.setup_configs()

    @property
    def app_config(self):
        return self._app_config

    @property
    def db_config(self):
        return self._db_config

    @property
    def mqtt_config(self):
        return self._mqtt_config

    @property
    def tv_config(self):
        return self._tv_config

    @property
    def web_config(self):
        return self._web_config

    def load_configs(self):
        self._app_config = config_utils.load_config_app()
        self._db_config = config_utils.load_config_db()
        self._mqtt_config = config_utils.load_config_mqtt()
        self._tv_config = config_utils.load_config_tv()
        self._web_config = config_utils.load_config_web()

    def setup_configs(self):
        try:
            self.load_configs()
        except (ModuleNotFoundError, FileNotFoundError):
            print("\n\nConfigs not created yet. Generating fresh files.\n\n")
            config_utils.copy_fresh_templates()
            try:
                self.load_configs()
            except (ModuleNotFoundError, FileNotFoundError):
                print("\n\nConfigs not found. Cannot continue.\n\n")
                sys.exit(1)
