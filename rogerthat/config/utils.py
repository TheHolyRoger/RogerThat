import os
import secrets
import shutil
import uuid
from rogerthat.utils.yaml import (
    load_yml_from_file,
    save_yml_to_file,
)


config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "configs")


def load_config(file, sample_mode=False):
    sample_files = ".sample" if sample_mode else ""
    return load_yml_from_file(os.path.join(config_dir, f"{file}{sample_files}.yml"))


def save_config(data, file, sample_mode=False):
    sample_files = ".sample" if sample_mode else ""
    return save_yml_to_file(data, os.path.join(config_dir, f"{file}{sample_files}.yml"))


def generate_api_key(existing_keys):
    new_api_key = None
    while not new_api_key:
        api_key = str(uuid.uuid4())
        if api_key not in existing_keys:
            new_api_key = api_key
    return new_api_key


def generate_quart_secrets():
    config = load_config("web_server")
    config["quart_secret_key"] = secrets.token_urlsafe(16)
    config["quart_auth_pep"] = secrets.token_urlsafe(16)
    save_config(config, "web_server")


def delete_sample_api_key():
    config = load_config("web_server")
    config["api_allowed_keys"].pop(0)
    save_config(config, "web_server")


def save_new_api_key():
    config = load_config("web_server")
    newkey = generate_api_key(config["api_allowed_keys"])
    config["api_allowed_keys"].append(newkey)
    save_config(config, "web_server")


def update_conf_from_template(conf_file):
    sample_config = load_config(conf_file, sample_mode=True)
    user_config = load_config(conf_file)
    for k in sample_config.keys():
        sample_config[k] = user_config.get(k, sample_config[k])
    save_config(sample_config, conf_file)


def copy_fresh_templates():
    for conf_file in os.listdir(config_dir):
        if ".sample" in conf_file:
            templ_conf = os.path.join(config_dir, conf_file)
            new_conf = os.path.join(config_dir, conf_file.replace(".sample", ""))
            if os.path.exists(new_conf):
                os.remove(new_conf)
            shutil.copy(templ_conf, new_conf)
    delete_sample_api_key()
    save_new_api_key()
    generate_quart_secrets()


def delete_existing_configs():
    for conf_file in os.listdir(config_dir):
        if ".sample" not in conf_file:
            os.remove(os.path.join(config_dir, conf_file))


def update_configs():
    config_list = [
        "database",
        "main_config",
        "tradingview",
        "web_server",
    ]
    for conf in config_list:
        update_conf_from_template(conf)
