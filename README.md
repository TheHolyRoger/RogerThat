# RogerThat

RogerThat is a standalone webserver designed for use with tradingview webhooks and forwarding them to hummingbot.

## Docker
### Installation

[Install Docker](https://docs.docker.com/get-docker/)

Download and extract this [whole repository](https://github.com/TheHolyRoger/RogerThat/archive/refs/heads/master.zip).

```bash
wget https://github.com/TheHolyRoger/RogerThat/archive/refs/heads/master.zip
unzip master.zip
```

Change directory:
```bash
cd RogerThat
```

Then run the following commands to build and run the docker image:

Linux/Mac
```bash
./scripts/start_docker.sh
```

Windows
```bash
./scripts/start_docker.bat
```

### Running

Run without re-building:

Linux/Mac
```bash
./scripts/start_docker.sh -d
```

Windows
```bash
./scripts/start_docker.bat -d
```

### Enabling HTTPS

Place both your certificate and key in `./certs` folder named `server.crt` and `server.key` ([LetsEncrypt](https://letsencrypt.org/getting-started/) is recommended).

Or run the following command to generate a self-signed key pair (requires openssl):

Linux/Mac
```bash
scripts/generate_self_signed_cert.sh
```
Windows
```bash
scripts/generate_self_signed_cert.bat
```

### Public access

Since TradingView requires a publicly accessible URL for webhook alerts, you'll need to use your own domain name, or your public IP address.

You'll also need to open up (and forward) port 80 (or 443 if using HTTPS) in your firewall/router to the machine running RogerThat.

(Do NOT open up port 10073 externally)

### Dynamic Domain Names

Services you can use for Dynamic DNS with a non-static public IP address are:

* [No-IP](https://www.noip.com/)
* [Afraid](https://afraid.org/)
* [Duck DNS](https://duckdns.org/)
* [Dynu](http://www.dynu.com/)

### Configuration

You can use the config setup script via docker by running the following command:

Linux/Mac
```bash
scripts/start_docker_setup_script.sh --help
```
Windows
```bash
scripts/start_docker_setup_script.bat --help
```

#### Change Hostname

Change the hostname to listen on for the public TradingView webhook with the following command:

Linux/Mac
```bash
scripts/start_docker_setup_script.sh --hostname yourhostname.com
scripts/start_docker_setup_script.sh --hostname 1.2.3.4
```
Windows
```bash
scripts/start_docker_setup_script.bat --hostname yourhostname.com
scripts/start_docker_setup_script.bat --hostname 1.2.3.4
```

## Source
### Installation

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

```bash
./scripts/update_environment.sh
```

Run the following command to generate the default configs:
```bash
scripts/setup.py -s
```

Edit the configs in `./configs` or via the `setup.py` command.

### Running

From source:

```bash
bin/start_rogerthat.py
```

## Usage

### TradingView Webhooks

Set up your TradingView alert URL like this:

```html
http://<public-ip-or-domain-name>/api/tv_webhook/?api_key=<tradingview-apikey>
```

Where `<public-ip-or-domain-name>` is your domain name or public IP address and `<tradingview-apikey>` is the generated api key found in `web_server.yml` under `api_allowed_keys_tv`.

### Hummingbot Connection

You can connect hummingbot with websockets to this URL:
```html
ws://localhost:10073/wss
```

### Test Connection

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

## License
[MIT](https://choosealicense.com/licenses/mit/)