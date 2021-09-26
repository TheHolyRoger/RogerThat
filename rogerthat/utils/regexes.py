import re


class regexes:
    valid_ws_channel_name = re.compile(r"^[\w\-]+$")
