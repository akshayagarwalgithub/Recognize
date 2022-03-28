from utils.log_formatter import ColorFormatter
import logging
class LogInstantiator:
    def get_logger(self, module_name):
        logger = logging.getLogger(module_name)
        logger.setLevel(logging.INFO)
        color_formatter = ColorFormatter("%(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(color_formatter)
        logger.addHandler(console_handler)

        return logger