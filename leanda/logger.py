import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace(
            "$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': MAGENTA,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        s = logging.Formatter.format(self, record)
        if self.use_color and record.levelname in COLORS:
            s = COLOR_SEQ % (
                30 + COLORS[record.levelname]) + s + RESET_SEQ
        return s


# Custom logger class with multiple destinations
class ColoredLogger(logging.Logger):
    FORMAT = "%(message)s"
    # FORMAT = "%(levelname)-18s  %(message)s $BOLD%(filename)s$RESET:%(lineno)d"
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

        fileHandler = logging.FileHandler("debug.log")
        fileHandler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s (%(filename)s)"))
        self.addHandler(fileHandler)

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(color_formatter)
        self.addHandler(consoleHandler)

        return


def initialize():
    logging.setLoggerClass(ColoredLogger)


# logging.basicConfig(filename='app.log', filemode='w',
#                     format='%(name)s - %(levelname)s - %(message)s')

# logFormatter = logging.Formatter(
#     "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# rootLogger = logging.getLogger()

# fileHandler = logging.FileHandler("app.log")
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)

# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)

# rootLogger.addHandler(logging.StreamHandler(sys.stdout))


# fileHandler = logging.FileHandler("debug.log")
# fileHandler.setFormatter(logging.Formatter("%(asctime)-8s [%(levelname)s] %(message)s"))

# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

# logging.basicConfig(
#     level=logger.info,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[
#         fileHandler,
#         consoleHandler
#     ]
# )
