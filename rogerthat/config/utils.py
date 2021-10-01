import os
import ruamel.yaml
import secrets
import shutil
import uuid
from rogerthat.utils.yaml import (
    load_yml_from_file,
    save_yml_to_file,
    yml_clear_list,
    yml_fix_list_comments,
    yml_add_to_list,
)


class config_utils:

    _config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "configs")
    _config_sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")

    # Config file names
    _conf_file_db = "database"
    _conf_file_main = "main_config"
    _conf_file_tv = "tradingview"
    _conf_file_web = "web_server"
    _conf_file_list = [_conf_file_db, _conf_file_main, _conf_file_tv, _conf_file_web]

    _auto_gen_str = "# This file is auto-generated, changes will be overwritten by .yml values\n\n"

    _ignore_keys = [
        "template_version",
    ]

    @classmethod
    def load_config(cls, file, sample_mode=False):
        dir_name = cls._config_sample_dir if sample_mode else cls._config_dir
        sample_files = ".sample" if sample_mode else ""
        return load_yml_from_file(os.path.join(dir_name, f"{file}{sample_files}.yml"))

    @classmethod
    def save_config(cls, data, file, sample_mode=False):
        dir_name = cls._config_sample_dir if sample_mode else cls._config_dir
        sample_files = ".sample" if sample_mode else ""
        return save_yml_to_file(data, os.path.join(dir_name, f"{file}{sample_files}.yml"))

    @classmethod
    def generate_api_key(cls, existing_keys):
        new_api_key = None
        while not new_api_key:
            api_key = str(uuid.uuid4())
            if api_key not in existing_keys:
                new_api_key = api_key
        return new_api_key

    @classmethod
    def generate_quart_secrets(cls):
        config = cls.load_config(cls._conf_file_web)
        config["quart_secret_key"] = secrets.token_urlsafe(16)
        config["quart_auth_pep"] = secrets.token_urlsafe(16)
        config["quart_auth_csalt"] = secrets.token_urlsafe(8)
        cls.save_config(config, cls._conf_file_web)

    @classmethod
    def save_new_api_key_tv(cls, clear=False):
        config = cls.load_config(cls._conf_file_web)
        newkey = cls.generate_api_key(config["api_allowed_keys_tv"])
        if clear:
            config["api_allowed_keys_tv"] = yml_clear_list(config["api_allowed_keys_tv"])
        config["api_allowed_keys_tv"] = yml_add_to_list(config["api_allowed_keys_tv"], newkey)
        cls.save_config(config, cls._conf_file_web)

    @classmethod
    def save_new_api_key_hbot(cls, clear=False):
        config = cls.load_config(cls._conf_file_web)
        newkey = cls.generate_api_key(config["api_allowed_keys_hbot"])
        if clear:
            config["api_allowed_keys_hbot"] = yml_clear_list(config["api_allowed_keys_hbot"])
        config["api_allowed_keys_hbot"] = yml_add_to_list(config["api_allowed_keys_hbot"], newkey)
        cls.save_config(config, cls._conf_file_web)

    @classmethod
    def update_conf_from_template(cls, conf_file):
        sample_config = cls.load_config(conf_file, sample_mode=True)
        user_config = cls.load_config(conf_file)
        for k in sample_config.keys():
            if k not in cls._ignore_keys:
                user_value = user_config.get(k, sample_config[k])
                if user_value and isinstance(sample_config[k], ruamel.yaml.comments.CommentedSeq):
                    new_list = ruamel.yaml.comments.CommentedSeq(user_value)
                    new_list._yaml_comment = sample_config[k].ca
                    yml_fix_list_comments(new_list)
                    sample_config[k] = new_list
                elif user_value:
                    sample_config[k] = user_value
        cls.save_config(sample_config, conf_file)
        if conf_file == cls._conf_file_web:
            cls.generate_env_nginx()
        elif conf_file == cls._conf_file_db:
            cls.generate_env_postgres()

    @classmethod
    def check_conf_version(cls, conf_file):
        sample_config = cls.load_config(conf_file, sample_mode=True)
        user_config = cls.load_config(conf_file)
        sample_version = sample_config.get("template_version")
        user_version = user_config.get("template_version")
        if sample_version != user_version:
            cls.update_conf_from_template(conf_file)

    @classmethod
    def save_new_hostname(cls, new_hostname_raw):
        new_hostname = new_hostname_raw
        split_host = new_hostname_raw.split("://")
        if len(split_host) > 1:
            new_hostname = split_host[1]
        new_hostname = new_hostname.split(":")[0]
        new_hostname = new_hostname.split("/")[0]
        config = cls.load_config(cls._conf_file_web)
        config["server_host"] = new_hostname
        cls.save_config(config, cls._conf_file_web)
        cls.generate_env_nginx()

    @classmethod
    def toggle_iptables(cls, enable=False):
        config = cls.load_config(cls._conf_file_web)
        config["protect_with_cloudflare_firewall_rules"] = bool(enable)
        cls.save_config(config, cls._conf_file_web)
        cls.generate_env_nginx()

    @classmethod
    def toggle_websocket_auth(cls, disable):
        config = cls.load_config(cls._conf_file_web)
        config["disable_websocket_authentication"] = bool(disable)
        cls.save_config(config, cls._conf_file_web)

    @classmethod
    def generate_env_postgres(cls, safe=False):
        pg_env_path = os.path.join(cls._config_dir, "env_postgres.env")
        if os.path.exists(pg_env_path) and safe:
            return
        config = cls.load_config(cls._conf_file_db)
        pg_user = config["database_user"]
        pg_pw = config["database_password"]
        with open(pg_env_path, "w+") as fp:
            fp.write(cls._auto_gen_str)
            fp.write("POSTGRES_DB=postgres\n")
            fp.write(f"POSTGRES_USER={pg_user}\n")
            fp.write(f"POSTGRES_PASSWORD={pg_pw}\n")

    @classmethod
    def generate_env_nginx(cls, safe=False):
        nginx_env_path = os.path.join(cls._config_dir, "env_nginx.env")
        if os.path.exists(nginx_env_path) and safe:
            return
        config = cls.load_config(cls._conf_file_web)
        hostname = config["server_host"]
        port = config["quart_server_port"]
        use_iptables = config["protect_with_cloudflare_firewall_rules"]
        with open(nginx_env_path, "w+") as fp:
            fp.write(cls._auto_gen_str)
            fp.write(f"HOSTNAME={hostname}\n")
            fp.write(f"API_PORT={port}\n")
            if use_iptables:
                fp.write("ADD_CLOUDFLARE_IPTABLES=1\n")

    @classmethod
    def copy_fresh_templates(cls, safe=False):
        configs_exist = False
        for conf_file in os.listdir(cls._config_sample_dir):
            if ".sample" in conf_file or ".env" in conf_file:
                templ_conf = os.path.join(cls._config_sample_dir, conf_file)
                new_conf = os.path.join(cls._config_dir, conf_file.replace(".sample", ""))
                if os.path.exists(new_conf):
                    if ".env" not in conf_file:
                        configs_exist = True
                    if safe or ".env" in conf_file:
                        continue
                    os.remove(new_conf)
                shutil.copy(templ_conf, new_conf)
        if not safe or not configs_exist:
            cls.save_new_api_key_tv(clear=True)
            cls.save_new_api_key_hbot(clear=True)
            cls.generate_quart_secrets()
        cls.generate_env_postgres()
        cls.generate_env_nginx()

    @classmethod
    def delete_existing_configs(cls):
        for conf_file in os.listdir(cls._config_dir):
            if ".sample" not in conf_file and (".yml" in conf_file or ".env" in conf_file):
                os.remove(os.path.join(cls._config_dir, conf_file))

    @classmethod
    def check_configs(cls):
        cls.copy_fresh_templates(True)
        for conf in cls._conf_file_list:
            cls.check_conf_version(conf)
        cls.generate_env_postgres()
        cls.generate_env_nginx()

    @classmethod
    def update_configs(cls):
        for conf in cls._conf_file_list:
            cls.update_conf_from_template(conf)

    # Individual config loaders
    @classmethod
    def load_config_app(cls):
        return cls.load_config(cls._conf_file_main)

    @classmethod
    def load_config_db(cls):
        return cls.load_config(cls._conf_file_db)

    @classmethod
    def load_config_tv(cls):
        return cls.load_config(cls._conf_file_tv)

    @classmethod
    def load_config_web(cls):
        return cls.load_config(cls._conf_file_web)
