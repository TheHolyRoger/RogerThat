class instance_wrapper:
    _shared_instance: "instance_wrapper" = None

    @classmethod
    def update_instance(cls, new_instance):
        cls._shared_instance = new_instance

    @classmethod
    def get_instance(cls) -> "instance_wrapper":
        if cls._shared_instance is None:
            raise Exception("instance_wrapper instance has not been set yet!")
        return cls._shared_instance
