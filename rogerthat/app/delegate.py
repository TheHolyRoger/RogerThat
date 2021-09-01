from rogerthat.utils.instance_wrapper import instance_wrapper


class AppWrap(instance_wrapper):
    @property
    def Main(self):
        return self.instance


App = AppWrap()
