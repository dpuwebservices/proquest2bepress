class MyException(Exception):
    pass


class P2BException(Exception):
    def __init__(self, message, filename):
        super(self.__class__, self).__init__(message)
        self.filename = filename


class InvalidConfig(Exception):
    pass