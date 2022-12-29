from decimal import Decimal as Dec

from quart import json


class JSONEncoder(json.JSONEncoder):

    def default(self, object_):
        if isinstance(object_, Dec):
            return str(object_)
        else:
            return super().default(object_)


class JSONDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.dec_to_str, *args, **kwargs)

    def dec_to_str(self, dec_):
        if '.' in dec_ and str(dec_).replace('.', '').isdigit():
            return Dec(str(dec_))
        else:
            return dec_
