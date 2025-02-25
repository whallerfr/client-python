import os
import logging

class Logger():
    def __init__(self, name: str, logger_path: str = None, level: int = logging.ERROR):
        self.current_logger = self.init(name, level, logger_path)

    def init(self, filename, level, logger_path = None):
        if logger_path is None:
            logger_path = os.path.abspath(os.getcwd()) + '/logs/'

        if os.path.exists(logger_path) == False:
            os.makedirs(logger_path, exist_ok=True)

        logger = logging.getLogger(filename)
        logger.setLevel(level)
        if logger.hasHandlers() == False:
            filepath = logger_path + filename + '.log'
            fh = logging.FileHandler(filepath)
            fh.setLevel(level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        return logger

    def debug(self, debug):
        if self.current_logger is None:
            return

        self.current_logger.debug(debug)

    def info(self, info):
        if self.current_logger is None:
            return

        self.current_logger.info(info)

    def warning(self, warning):
        if self.current_logger is None:
            return

        self.current_logger.warning(warning)

    def error(self, error):
        if self.current_logger is None:
            return

        self.current_logger.error(error)
