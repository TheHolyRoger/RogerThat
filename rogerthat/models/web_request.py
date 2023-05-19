from rogerthat.config.config import Config
from rogerthat.logging.configure import AsyncioLogger

logger = AsyncioLogger.get_logger_main(__name__)


class web_request:
    def __init__(self,
                 from_quart=None):
        self._quart_request = None
        self._request_args_data = None
        self._request_args_keys = None
        self._json_data = None
        self._source_address = None
        self._user_agent = None
        self._origin = None
        self._referrer = None
        self._url = None
        self._url_root = None
        self._base_url = None
        self._full_path = None
        self._query_string = None
        self._args = None
        self._content_type = None
        self._cookies = None
        self._headers = None
        if from_quart:
            self._quart_request = from_quart
            self._source_address = from_quart.access_route[0]
            self._user_agent = from_quart.user_agent.string.lower().strip()
            self._origin = from_quart.origin
            self._referrer = from_quart.referrer
            self._url = from_quart.url
            self._url_root = from_quart.url_root
            self._base_url = from_quart.base_url
            self._full_path = from_quart.full_path
            self._query_string = from_quart.query_string
            self._args = from_quart.args
            self._content_type = from_quart.content_type
            self._cookies = from_quart.cookies
            self._headers = from_quart.headers

    @property
    def json_data(self):
        return self._json_data

    async def build_request_args(self):
        form_data = await self._quart_request.form
        if len(form_data) > 0:
            self._request_args_data = form_data
        if len(self._quart_request.args) > 0:
            if self._request_args_data:
                self._request_args_data = {**self._request_args_data, **self._quart_request.args}
            else:
                self._request_args_data = {**self._quart_request.args}
        if self._request_args_data:
            self._request_args_keys = list(self._request_args_data.keys())
        return True

    async def build_json_data(self):
        self._json_data = await self._quart_request.json
        return True

    def check_valid_user_agent(self):
        return self._user_agent and self._user_agent in Config.get_inst().accepted_user_agents_tv

    def check_valid_content_type(self):
        return self._content_type and (self._content_type.startswith('application/json') or
                                       self._content_type.startswith('text/plain'))

    def check_valid_api_key_tv(self):
        return (self._request_args_keys and
                "api_key" in self._request_args_keys and
                self._request_args_data["api_key"] in Config.get_inst().api_allowed_keys_tv)

    def check_valid_json(self):
        if not self._json_data:
            return False
        if isinstance(self._json_data, list):
            return all(['topic' in list(jdata.keys()) for jdata in self._json_data])
        return 'topic' in list(self._json_data.keys())

    async def check_is_valid(self,
                             for_tv_api=False,):
        if for_tv_api and not self.check_valid_user_agent():
            logger.warning("Invalid User Agent detected.")
            await self.log_request_full()
            return False
        if for_tv_api and not self.check_valid_content_type():
            logger.warning("Invalid Content type detected.")
            await self.log_request_full()
            return False
        if not self._request_args_data:
            await self.build_request_args()
        if for_tv_api and not self.check_valid_api_key_tv():
            logger.warning("Invalid api key detected.")
            await self.log_request_full()
            return False
        if for_tv_api and not self._json_data:
            await self.build_json_data()
        if not for_tv_api or self.check_valid_json():
            return True
        else:
            logger.warning("Invalid json detected.")
        return False

    async def log_request_full(self):
        line_separation_start = str('>' * 40)
        line_separation_end = str('<' * 40)
        line_break = str('\n' * 4)
        log_lines = [line_separation_start]
        log_lines.append(f"Request from Address: {self._source_address}")
        log_lines.append(f"User Agent: {self._user_agent}")
        log_lines.append(f"Origin: {self._origin}, Referrer: {self._referrer}")
        log_lines.append(f"Full URL: {self._url}")
        log_lines.append(f"URL Root: {self._url_root}")
        log_lines.append(f"Base URL: {self._base_url}")
        log_lines.append(f"Full Path: {self._full_path}")
        log_lines.append(f"Query string: {self._query_string}")
        log_lines.append(f"Query Params: {self._args}")
        log_lines.append(f"Full Params: {self._request_args_data}")
        try:
            log_lines.append(f"Data: {await self._quart_request.data}")
        except Exception as e:
            logger.error(f"Data Exc: {e}")
        try:
            log_lines.append(f"Full Data: {await self._quart_request.get_data()}")
        except Exception as e:
            logger.error(f"Full Data Exc: {e}")
        try:
            log_lines.append(f"JSON: {await self._quart_request.json}")
        except Exception as e:
            logger.error(f"JSON Exc: {e}")
        log_lines.append(f"Content Type: {self._content_type}")
        log_lines.append(f"Cookies: {self._cookies}")
        log_lines.append(f"Full Headers {'>' * 10}")
        for header in self._headers:
            log_lines.append(f"    {header[0]}: {header[1]}")
        log_lines.append(line_separation_end)
        log_string = "\n".join(log_lines)
        logger.debug(f"{line_break}{log_string}{line_break}")
        return True

    def __repr__(self):
        return f"{vars(self)}"
