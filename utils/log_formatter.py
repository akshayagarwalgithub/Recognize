import logging
from colorama import init, Fore, Back, Style

init(autoreset=True)


class ColorFormatter(logging.Formatter):

    COLORS = {
        "DEBUG": Fore.BLACK,
        "INFO": Fore.BLUE,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED + Style.BRIGHT,
        "CRITICAL": Fore.WHITE + Style.BRIGHT + Back.RED
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        if color:
            record.name = color + record.name
            record.levelname = color + record.levelname
            record.msg = color + record.msg
        return logging.Formatter.format(self, record)
