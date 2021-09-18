# RogerThat

RogerThat is a standalone webserver designed for use with tradingview webhooks and forwarding them to hummingbot.

## Docker
### Installation

Make sure you have docker installed, download and extract this whole repository.

```bash
wget https://github.com/TheHolyRoger/RogerThat/archive/refs/heads/master.zip
unzip master.zip
```

Change directory:
```bash
cd RogerThat
```

Then run the following command to build and run the docker image:
```bash
./scripts/install_docker.sh
```

Edit the HOSTNAME to listen on for the public TradingView webhook in the `./configs/env_nginx.env` file.

### Usage

```bash
docker compose up
```

## Source
### Installation

Clone this repository.

```bash
git clone git@github.com:TheHolyRoger/RogerThat.git
```

Change directory:
```bash
cd RogerThat
```

Set up and activate the environment with the following command.

```bash
./scripts/update_environment.sh
```

Run the following command to generate the default configs:
```bash
scripts/setup.py -s
```

Edit the configs in `./configs` or via the `setup.py` command.

### Usage

From source:

```bash
bin/start_rogerthat.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)