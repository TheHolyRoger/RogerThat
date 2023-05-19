from rogerthat.utils.class_helpers import no_setters


class time_in_seconds_constants(no_setters):
    __attr_descriptor__ = "time constant"
    _minute = (60)
    _hour = int(_minute * 60)
    _day = int(_hour * 24)
    _week = int(_day * 7)
    _month = int(_day * 30)
    _year = int(_day * 365)


time_in_seconds = time_in_seconds_constants.get_inst()
