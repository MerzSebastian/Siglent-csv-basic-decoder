class Logger:

    def __init__(self):
        self.loggerActive = True

    def log(self, value):
        if self.loggerActive:
            print(value)

    def on(self):
        self.loggerActive = True

    def off(self):
        self.loggerActive = False
