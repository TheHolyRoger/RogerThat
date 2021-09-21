# RogerThat

**RogerThat** is a standalone webserver designed to receive **TradingView** webhooks (or similar) and forward them to **Hummingbot** via websockets or REST queries.

# Docker
## Installation

[**Install Docker**](https://docs.docker.com/get-docker/)

Download and extract this [**whole repository**](https://github.com/TheHolyRoger/RogerThat/archive/refs/heads/master.zip).

<details>
<summary>Linux/Mac</summary>

```bash
wget https://github.com/TheHolyRoger/RogerThat/archive/refs/heads/master.zip
unzip master.zip
```

Change directory:
```bash
cd RogerThat
```

</details>
<details>
<summary>Windows</summary>

```bat
bitsadmin /transfer dlrogerthat /download /priority normal https://github.com/TheHolyRoger/RogerThat/archive/refs/heads/master.zip %UserProfile%\RogerThat.zip
```

Extract the zip file manually.

Change directory:
```bash
cd RogerThat
```

</details>

Then run the following commands to launch the docker image:

<details>
<summary>Linux/Mac</summary>

```bash
./scripts/start_docker.sh
```
</details>
<details>
<summary>Windows</summary>

![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) :warning: **If using windows, make sure to run the .bat scripts using windows CMD, not "Git Bash".**

Use git bash only for `git` commands, do not run these scripts from git bash as they will not work.

```bat
./scripts/start_docker.bat
```
</details>

___

## Running

Run without re-building:

<details>
<summary>Linux/Mac</summary>

```bash
./scripts/start_docker.sh -d
```
</details>
<details>
<summary>Windows</summary>

```bat
scripts\start_docker.bat -d
```
</details>

___

## Public access

<details>
<summary>Expand ...</summary>

Since **TradingView** requires a publicly accessible URL for webhook alerts, you'll need to use your own domain name, or your public IP address.

You'll also need to open up (and forward) port **80** (or **443** if using HTTPS) in your firewall/router to the machine running **RogerThat**.

**(Do NOT open up port 10073 externally)**

### Dynamic Domain Names

Services you can use for dynamic DNS with a non-static public IP address are:

* [No-IP](https://www.noip.com/)
* [Afraid](https://afraid.org/)
* [Duck DNS](https://duckdns.org/)
* [Dynu](http://www.dynu.com/)

### Enabling HTTPS

Place both your certificate and key in `./certs` folder named `server.crt` and `server.key` ([LetsEncrypt](https://letsencrypt.org/getting-started/) is recommended).

Or run the following command to generate a self-signed key pair:

Linux/Mac
```bash
scripts/generate_self_signed_cert.sh
```

Windows
```bat
scripts\generate_self_signed_cert.bat
```
</details>

___

## Configuration

You can use the config setup script via docker by running the following commands:

<details>
<summary>Linux/Mac</summary>

```bash
scripts/setup_config.sh --help
```
</details>
<details>
<summary>Windows</summary>

```bat
scripts\setup_config.bat --help
```
</details>

### Change Hostname

Change the hostname to listen on for the public **TradingView** webhook with the following command:

<details>
<summary>Linux/Mac</summary>

```bash
scripts/setup_config.sh --hostname yourhostname.com
scripts/setup_config.sh --hostname 1.2.3.4
```
</details>
<details>
<summary>Windows</summary>

```bat
scripts\setup_config.bat --hostname yourhostname.com
scripts\setup_config.bat --hostname 1.2.3.4
```
</details>

___

# Source

<details>
<summary>Steps to install from source instead of docker ...</summary>

## Installation

[Install Miniconda](https://docs.conda.io/en/latest/miniconda.html) (or Anaconda)

Clone this repository.

```bash
git clone git@github.com:TheHolyRoger/RogerThat.git
```

Change directory:
```bash
cd RogerThat
```

Set up and activate the environment with the following command.

<details>
<summary>Linux/Mac</summary>

```bash
./scripts/update_environment.sh
```
</details>
<details>
<summary>Windows</summary>

```bat
scripts\update_environment.bat
```
</details>

Run the following command to generate the default configs:
```bash
scripts/setup.py -s
```

Edit the configs in `./configs` or via the `setup.py` command.

___

## Running

From source:

```bash
bin/start_rogerthat.py
```
</details>

___

# Usage

## TradingView Webhooks

Set up your **TradingView** alert URL like this:

```html
http://<public-ip-or-domain-name>/api/tv_webhook/?api_key=<tradingview-apikey>
```

Where `<public-ip-or-domain-name>` is your domain name or public IP address and `<tradingview-apikey>` is the generated api key found in `web_server.yml` under `api_allowed_keys_tv`.

### JSON Data for TradingView alerts.

Alerts must be formatted as JSON, the only required parameter is `name`.
*(this parameter key name is configurable in `configs/tradingview.yml`)*

The `name` key or one of the `tradingview_descriptor_fields` must be present in the JSON data to be accepted, but the value can be null or empty.

Using an empty value for `name` ignores **Hummingbot**'s *Remote Command Executor* routing names.

<details>
<summary>Example alert data:</summary>

Simple Start command

```json
{
    "name": "hummingbot_instance_1",
    "command": "start",
}
```

Simple Stop command

```json
{
    "name": "hummingbot_instance_1",
    "command": "stop",
}
```

Alert with all fields using Pine variables

```json
{
    "name": "hummingbot_instance_1",
    "timestamp": "{{timenow}}",
    "exchange": "{{exchange}}",
    "symbol": "{{ticker}}",
    "interval": "{{interval}}",
    "price": "{{close}}",
    "volume": "{{volume}}",
    "command": "{{strategy.market_position}}",
    "inventory": "{{strategy.order.comment}}"
}
```

</details>

___

## Hummingbot Connection

You can connect the **Hummingbot** _Remote Command Executor_ to the **RogerThat** websocket with this URL:
```html
ws://localhost:10073/wss
```

### Example Config

<details>
<summary>Example Config ...</summary>

Use something like the following config to connect **RogerThat** to **Hummingbot** via the **Remote Command Executor**.

```yaml
# Remote commands
remote_commands_enabled: true
remote_commands_api_key: a9ba4b61-6f6d-41cf-85c3-7cfdfcbea0f3
remote_commands_ws_url: ws://localhost:10073/wss
remote_commands_routing_name: hummingbot_instance_1
remote_commands_ignore_first_event: true
remote_commands_translate_commands:
  long: start
  short: stop
```

</details>

___

## Test Connection

<details>
<summary>Test Connection ...</summary>

Test the websocket feed in your browser with this js code:

```javascript
var ws = new WebSocket('ws://localhost:10073/wss');
ws.onmessage = function (event) {
    console.log(event.data);
};
```

Or run the python test listener:

```bash
python tests/test_websocket.py
```

Or test the REST url here:

```html
http://localhost:10073/api/hbot/?api_key=<hummingbot-apikey>
```

Where `<hummingbot-apikey>` is the generated api key found in `web_server.yml` under `api_allowed_keys_hbot`.

</details>

___

# License
[MIT](https://choosealicense.com/licenses/mit/)