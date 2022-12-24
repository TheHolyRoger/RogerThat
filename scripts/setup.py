#!/usr/bin/env python
import argparse
import path_util  # noqa: F401
from rogerthat.config.utils import config_utils
from rogerthat.utils.splash import splash_msg


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
    parser.add_argument('--hostname', dest="hostname", type=str,
                        help="Update hostname.")
    parser.add_argument('--generate-api-key-tv', '-t', dest="generate_api_key_tv", action='store_true',
                        help="Generate and save a new TradingView api key to the config.")
    parser.add_argument('--generate-quart-secrets', '-q', dest="generate_quart_secrets", action='store_true',
                        help="Generate and save new quart secrets.")
    parser.add_argument('--enable-iptables-cloudflare', dest="enable_iptables", action='store_true',
                        help="Enable iptables firewall rules to only allow Cloudflare traffic.")
    parser.add_argument('--disable-iptables-cloudflare', dest="disable_iptables", action='store_true',
                        help="Disable iptables firewall rules to only allow Cloudflare traffic.")
    parser.add_argument('--print-splash', dest="print_splash", action='store_true',
                        help="Print launch screen.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.print_splash:
        print(splash_msg)
        quit()
    if args.delete_configs:
        config_utils.delete_existing_configs()
    if args.setup_configs:
        config_utils.copy_fresh_templates()
    if args.setup_configs_if_blank:
        config_utils.check_configs()
    if args.generate_api_key_tv:
        config_utils.check_configs()
        config_utils.save_new_api_key_tv()
    if args.generate_quart_secrets:
        config_utils.check_configs()
        config_utils.generate_quart_secrets()
    if args.hostname:
        config_utils.check_configs()
        config_utils.save_new_hostname(args.hostname)
    if args.enable_iptables or args.disable_iptables:
        config_utils.check_configs()
        config_utils.toggle_iptables(enable=True if args.enable_iptables else False)
    if args.update_configs:
        config_utils.check_configs()
        config_utils.update_configs()
