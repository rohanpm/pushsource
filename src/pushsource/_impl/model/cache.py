class SingleValueCacher(object):
    __slots__ = ("last_value", "type", "converter")

    def __init__(self, type, converter=lambda x: x):
        self.last_value = None
        self.type = type
        self.converter = converter

    def __call__(self, value):
        value = self.converter(value)

        if not isinstance(value, self.type):
            return value

        last = self.last_value
        if value == last:
            return last

        self.last_value = value
        return value
