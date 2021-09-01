import argparse
import os
import shutil
import uuid
import path_util  # noqa: F401
from rogerthat.config.utils import config_dir, load_config, save_config


def parse_args():
    parser = argparse.ArgumentParser(description='RogerThat configuration setup.')
    parser.add_argument('--setup-configs', '-s', dest="setup_configs", action='store_true',
                        help="Clone initial config templates.")
    parser.add_argument('--update-configs', '-u', dest="update_configs", action='store_true',
                        help="Update config files from templates.")
    parser.add_argument('--generate-api-key', '-g', dest="generate_api_key", action='store_true',
                        help="Generate and save a new api key to the config.")
    return parser.parse_args()


def generate_api_key(existing_keys):
    new_api_key = None
    while not new_api_key:
        api_key = str(uuid.uuid4())
        if api_key not in existing_keys:
            new_api_key = api_key
    return new_api_key


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


def update_configs():
    config_list = [
        "database",
        "main_config",
        "tradingview",
        "web_server",
    ]
    for conf in config_list:
        update_conf_from_template(conf)


if __name__ == "__main__":
    args = parse_args()
    if args.generate_api_key:
        save_new_api_key()
    if args.setup_configs:
        copy_fresh_templates()
    if args.update_configs:
        update_configs()
