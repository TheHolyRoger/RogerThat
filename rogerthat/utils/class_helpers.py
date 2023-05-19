class no_setters(object):
    _shared_instance: "no_setters" = None

    @classmethod
    def get_inst(cls) -> "no_setters":
        if cls._shared_instance is None:
            cls._shared_instance = cls()
        return cls._shared_instance

    def __init__(self):
        pass

    def __getattribute__(self, name):
        varname = f"_{name}" if not name.startswith('_') else name
        try:
            attr_tag = super(no_setters, self).__getattribute__("__attr_descriptor__")
        except AttributeError:
            attr_tag = "Attribute"
        err = f"{name} is an invalid {attr_tag}."
        try:
            return super(no_setters, self).__getattribute__(varname)
        except AttributeError:
            pass
        raise AttributeError(err)

    def __setattr__(self, name, value):
        return False
