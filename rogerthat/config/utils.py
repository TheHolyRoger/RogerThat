import os
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
