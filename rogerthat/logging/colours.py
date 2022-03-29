import logging


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[0m"
COLOUR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_colour=True):
    if use_colour:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLOURS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


class ColouredFormatter(logging.Formatter):
    def __init__(self, msg, use_colour=True):
        logging.Formatter.__init__(self, formatter_message(msg, use_colour=use_colour))
        self.use_colour = use_colour

    def format(self, record):
        levelname = record.levelname
        message = record.msg
        if self.use_colour and levelname in COLOURS:
            levelname_colour = COLOUR_SEQ % (30 + COLOURS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_colour
            if levelname == 'ERROR':
                record.msg = COLOUR_SEQ % (30 + RED) + message + RESET_SEQ
        formatted_record = logging.Formatter.format(self, record)
        # Reset original level
        record.levelname = levelname
        record.msg = message
        return formatted_record
