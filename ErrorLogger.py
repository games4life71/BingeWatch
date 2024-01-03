from datetime import datetime

"""
This class is used to log all warnings/errors to a file
"""


class ErrorLogger:
    def __init__(self):
        self.PATH = "logs"
        self.errorLog = []

    def log(self, error):
        # log an error and the time it occured
        self.errorLog.append((error, datetime.now().time()))

    def printLog(self):
        for error in self.errorLog:
            print(error)

    def log_to_file(self):
        name = self.PATH + "/error_" + str(datetime.today()).replace(' ', '').replace(':', '-') + ".txt"
        with open(name, "w") as f:
            for error in self.errorLog:
                # TODO append the time of which the error occured
                f.write(str(error[1]))
                f.write(" " + str(error[0]))
                f.write("\n")
