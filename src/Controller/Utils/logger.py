


class Logger:
    def __init__(self, debug):
        self._debug = debug

    def info(self, msg):
        print("INFO:" + msg)

    def error(self, msg):
        print("ERROR:" + msg)

    def debug(self, msg):
        if self._debug:
            print("DEBUG:" + msg)


