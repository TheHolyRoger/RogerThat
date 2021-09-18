# RogerThat

RogerThat is a standalone webserver designed for use with tradingview webhooks and forwarding them to hummingbot.

## Installation

### Source Installation

Set up and activate the environment with the following command.

```bash
./scripts/update_environment.sh
```

Run the following command to generate the default configs:
```bash
scripts/setup.py -s
```

Edit the configs in `./configs` or via the `setup.py` command.

### Docker Installation

Run the following command to build and run the docker image:
```bash
./scripts/install_docker.sh
```

Edit the HOSTNAME to listen on for the public TradingView webhook in the `./configs/env_nginx.env` file.

## Usage

From source:

```bash
bin/start_rogerthat.py
```

With docker:

```bash
docker compose up
```

## License
[MIT](https://choosealicense.com/licenses/mit/)