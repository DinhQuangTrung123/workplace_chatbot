import logging, os

class Logger():
    def init(self):
        self.logger = None

    def logtoFile(self, log_name = 'server.log'):
        console = True
        self.logger = logging.getLogger('log')
        file_logger = logging.FileHandler(os.path.join('log_file',log_name), encoding='utf-8')
        NEW_FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
        file_logger_format = logging.Formatter(NEW_FORMAT)


        file_logger.setFormatter(file_logger_format)


        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(file_logger)
        self.logger.setLevel(logging.INFO)

        if console:
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(message)s')
            console.setFormatter(formatter)
            self.logger.addHandler(console)
        return self.logger


logger = Logger().logtoFile()