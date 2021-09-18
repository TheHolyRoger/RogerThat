# RogerThat

RogerThat is a standalone webserver designed for use with tradingview webhooks and forwarding them to hummingbot.

## Installation

Set up and activate the environment with the following command.

```bash
./scripts/install_environment.sh
```

Run the following command to generate the default configs:
```bash
scripts/setup.py -s
```

Edit the configs in `./configs` or via the `setup.py` command.

### Docker Installation

Edit the HOSTNAME in the `./configs/env_nginx.env` file.

Run the following command to build the docker image:
```bash
docker build -t rogerthat:latest
```

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