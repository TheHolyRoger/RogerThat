#!/usr/bin/env python
import argparse
import path_util  # noqa: F401
from rogerthat.config.utils import (
    save_new_api_key,
    generate_quart_secrets,
    copy_fresh_templates,
    delete_existing_configs,
    update_configs,
)


def parse_args():
    parser = argparse.ArgumentParser(description='RogerThat configuration setup.')
    parser.add_argument('--setup-configs', '-s', dest="setup_configs_if_blank", action='store_true',
                        help="Clone initial config templates.")
    parser.add_argument('--setup-configs-force', '-f', dest="setup_configs", action='store_true',
                        help="Clone initial config templates (force).")
    parser.add_argument('--delete-configs', '-d', dest="delete_configs", action='store_true',
                        help="Delete existing configs.")
    parser.add_argument('--update-configs', '-u', dest="update_configs", action='store_true',
                        help="Update config files from templates.")
    parser.add_argument('--generate-api-key', '-g', dest="generate_api_key", action='store_true',
                        help="Generate and save a new api key to the config.")
    parser.add_argument('--generate-quart-secrets', '-q', dest="generate_quart_secrets", action='store_true',
                        help="Generate and save new quart secrets.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.delete_configs:
        delete_existing_configs()
    if args.setup_configs:
        copy_fresh_templates()
    if args.setup_configs_if_blank:
        copy_fresh_templates(True)
    if args.generate_api_key:
        save_new_api_key()
    if args.generate_quart_secrets:
        generate_quart_secrets()
    if args.update_configs:
        update_configs()
