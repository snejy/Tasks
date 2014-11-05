import logging


class Logger():


    def __init__(self, logfilename, logger_name):
        self.logfile = logfilename
        self.logger_name = logger_name

    def log(self, arguments, level = "info", format_with = '%(asctime)s %(message)s'):

        self.logger = logging.getLogger(self.logger_name)
        logging.basicConfig(filename = self.logfile, format = format_with)

        if type(arguments) == list:
            arguments = "  ".join(arguments)

        if level == "warning":
            self.logger.setLevel(logging.WARNING)
            self.logger.warning(arguments)

        elif level == "error":
            self.logger.setLevel(logging.ERROR)
            self.logger.error(arguments)

        elif level == "exception":
            self.logger.setLevel(logging.CRITICAL)
            self.logger.exception(arguments)

        else:
            self.logger.setLevel(logging.INFO)
            self.logger.info(arguments)


if __name__ == '__main__':
    pass
