# ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Important!! RogerThat has been rewritten for MQTT!
## Setup has completely changed to support MQTT with Hummingbot's new MQTT Bridge

# RogerThat

**RogerThat** is a standalone python web server designed to receive **TradingView** alerts (or similar) and forward them to **Hummingbot**.

**TradingView** is a widely used market market tracker that allows users to create, share and use custom strategies but is quite limited in how it can be "plugged in" or connected to other services. It does however allow the creation of "**Alerts**" which can send data to a Webhook (requires a public-facing URL).

**RogerThat** facilitates the collection and forwarding of these **TradingView Alerts** to **Hummingbot** via the **MQTT Bridge** module, which listens to **RogerThat** via subscribed MQTT topics.

Whilst RogerThat's purpose is to bridge **TradingView** and **Hummingbot**, it can work as a gateway / bridge between any service that sends data via Webhooks (to a public URL) and serve / route them to *multiple* **Hummingbot** instances or connected MQTT clients.

##### Menu

- [Docker](#docker)
  * [Installation](#installation)
  * [Running](#running)
  * [Stopping](#stopping)
  * [Configuration](#configuration)
    + [Public access](#public-access)
- [Usage](#usage)
  * [TradingView Webhooks](#tradingview-webhooks)
  * [Hummingbot Connection](#hummingbot-connection)
  * [Test Connection](#test-connection)
- [Source Installation (ADVANCED!!!)](#source-installation-advanced)

# Docker
## Installation

[**Install Docker**](https://docs.docker.com/engine/install/)

[**Install Docker Compose**](https://docker-docs.netlify.app/compose/install/#install-compose)

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **Be sure to use the latest docker-compose version number when installing.**

[**Fix Docker Permissions**](https://docs.docker.com/engine/install/linux-postinstall/)

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **When running on Linux be sure to apply the post install steps or you WILL run into permission errors.**

Download and extract this [**whole repository**](https://github.com/{{repository.name}}/archive/refs/heads/{{current.branch}}.zip).

<details>
<summary>Linux/Mac</summary>

```bash
wget https://github.com/{{repository.name}}/archive/refs/heads/{{current.branch}}.zip
unzip {{current.branch}}.zip
```

Change directory:
```bash
cd RogerThat-{{current.branch}}
```

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **You must always run scripts from the main RogerThat directory, do not switch to the `scripts` directory**

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **Do not run as root!!!**

</details>
<details>
<summary>Windows</summary>

Manually download and extract the [**repository zip file**](https://github.com/{{repository.name}}/archive/refs/heads/{{current.branch}}.zip).

Open up Windows CMD and **switch directory to the extracted zip folder**.

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **You must always run scripts from the main project directory, do not switch to the `scripts` directory**

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **If using Ubuntu WSL with Docker for Windows, you must enable permissions first, [see here](https://stackoverflow.com/a/50856772/16574146)**

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

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **If using windows, make sure to run the .bat scripts using windows CMD prompt, not "Git Bash".**

Use git bash only for `git` commands, do not run RogerThat scripts from git bash as they will not work.

```bat
scripts\start_docker.bat
```
</details>

___

## Running

<details>
<summary>Linux/Mac</summary>

```bash
./scripts/start_docker.sh
```

OR as daemon (in background):

```bash
./scripts/start_docker.sh -d
```
</details>
<details>
<summary>Windows</summary>

```bat
scripts\start_docker.bat
```

OR as daemon (in background):

```bat
scripts\start_docker.bat -d
```
</details>

Upon successful launch, navigating to `http://localhost/` (or your public domain) in your browser will show a 404 not found page.

___

## Stopping

Press ctrl+c if running interactively, or run the following command to stop RogerThat:
```bash
docker-compose stop
```

___

## Configuration

You can use the config setup script via docker by running the following commands:

<details>
<summary>Linux/Mac</summary>

```bash
scripts/setup_config.sh --help
```

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **Do not run the setup script via python, always run it via `scripts/setup_config.sh`.**

</details>
<details>
<summary>Windows</summary>

```bat
scripts\setup_config.bat --help
```

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **Do not run the setup script via python, always run it via `scripts\setup_config.bat`.**

</details>

___

### Public access

<details>
<summary>Expand ...</summary>

Since **TradingView** requires a publicly accessible URL for webhook alerts, you'll need to use your own domain name, or your public IP address.

You'll also need to open up (and forward) port **80** (or **443** if using HTTPS) in your firewall/router to the machine running **RogerThat**.

It is recommended to use **Cloudflare** proxied with **HTTPS** to mask your IP address.

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **You must change/set your hostname before enabling HTTPS with letsencrypt**

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **(Do NOT open up port 10073 externally)**

#### Change Hostname

<details>
<summary>Expand ...</summary>

Change the hostname to listen on for the public **TradingView** webhook with the following commands:

(Do not use a full URL here, the hostname is the part of the URL after https:// and before any other slashes)

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

If using your own domain name, it is recommended to use a long and not obvious subdomain as the hostname eg: `thereisnotraderhere.mydomain.com`.

</details>

#### Cloudflare (Recommended)

<details>
<summary>Expand ...</summary>

It is recommended to use [Cloudflare](https://www.cloudflare.com/) to proxy and mask your IP address in production since public access must be exposed.

You can use services like [DNS-o-matic](https://dnsomatic.com/) with your home dynamic IP to keep it updated and proxied with [Cloudflare](https://www.cloudflare.com/).

[More information in the help article here](https://support.cloudflare.com/hc/en-us/articles/360020524512-Manage-dynamic-IPs-in-Cloudflare-DNS-programmatically#h_161458650101544484552881)

</details>

#### Dynamic Domain Names (Optional)

<details>
<summary>Expand ...</summary>

Services you can use for dynamic DNS with a non-static public IP address are:

* [DNS-O-matic](https://dnsomatic.com/) (Recommended, with Cloudflare)
* [No-IP](https://www.noip.com/)
* [Afraid](https://afraid.org/)
* [Duck DNS](https://duckdns.org/)
* [Dynu](http://www.dynu.com/)

</details>

#### Enabling HTTPS (Recommended, required for Cloudflare)

<details>
<summary>Expand ...</summary>

To setup ([LetsEncrypt](https://letsencrypt.org/getting-started/) run the following commands.

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **You must set your hostname first and forward port 80 on your firewall!**

<details>
<summary>Linux/Mac</summary>

```bash
scripts/generate_cert_letsencrypt.sh
```

</details>
<details>
<summary>Windows</summary>

```bat
scripts/generate_cert_letsencrypt.bat
```
</details>

Or run the following command to generate a self-signed key pair:

<details>
<summary>Linux/Mac</summary>

```bash
scripts/generate_cert_self_signed.sh
```

</details>
<details>
<summary>Windows</summary>

```bat
scripts\generate_cert_self_signed.bat
```
</details>

After enabling HTTPS you can now forward port 443, close port 80 and start RogerThat.

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **It is recommended to close port 80**

</details>

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

Alerts must be formatted as JSON, the only required parameter is `topic`.

The `topic` key must be present in the JSON data to be accepted.

<details>
<summary>Example alert data:</summary>

Simple Start command

```json
{
    "topic": "hbot/hummingbot_instance_1/start",
    "log_level": "DEBUG"
}
```

Simple Stop command

```json
{
    "topic": "hbot/hummingbot_instance_1/stop",
    "skip_order_cancellation": false
}
```

Advanced alert with all fields using Pine variables

```json
{
    "topic": "hbot/hummingbot_instance_1/external/events/my_event",
    "type": "external_event",
    "timestamp": "{{timenow}}",
    "sequence": "{{timenow}}",
    "data": {
        "exchange": "{{exchange}}",
        "symbol": "{{ticker}}",
        "interval": "{{interval}}",
        "price": "{{close}}",
        "volume": "{{volume}}",
        "position": "{{strategy.market_position}}",
        "inventory": "{{strategy.order.comment}}"
    }
}
```

</details>

___

## Hummingbot Connection

Connect the **Hummingbot** _MQTT Bridge_ and **RogerThat** to the same MQTT Broker.

### Example Config

<details>
<summary>Example Config ...</summary>

Use something like the following config to connect **RogerThat** to **Hummingbot** via the **MQTT Bridge**.

This config is found inside your main hummingbot folder then `conf\conf_client.yml`

```yaml
# Remote commands
mqtt_bridge:
  mqtt_host: localhost
  mqtt_port: 1883
  mqtt_autostart: true
```

</details>


### Command Shortcuts

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) :warning: **This isn't yet implemented.**

<details>
<summary>Expand ...</summary>

Command shortcuts can be defined in Hummingbot's `conf_global.yml`, for more information see here: https://docs.hummingbot.io/operation/config-files/#create-command-shortcuts

</details>

___

## Test Connection

<details>
<summary>Test Connection ...</summary>

To test basic connection, use any MQTT client and connect to the same broker as RogerThat, then subscribe to the `rogerthat/#` topic.

There is also a small python script in the `examples/` folder which can be used to mimic a TradingView alert. You'll then see the MQTT message if you subscribe to your chosen topic.

</details>

___

# Source Installation (ADVANCED!!!)

<details>
<summary>Steps to install from **source** instead of docker ...</summary>

## Installation

[Install Miniconda](https://docs.conda.io/en/latest/miniconda.html) (or Anaconda)

Clone this repository.

```bash
git clone git@github.com:{{repository.name}}.git
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

# License
[MIT](https://choosealicense.com/licenses/mit/)