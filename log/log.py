import logging
import logging.handlers as handlers

class CustomFormatter(logging.Formatter):
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    CRITICAL = "\x1b[31;1m"
    format = "%(message)s"

    FORMAT = {
        logging.DEBUG: OKCYAN + format + ENDC,
        logging.INFO: OKGREEN + format + ENDC,
        logging.WARN: WARNING + format + ENDC,
        logging.ERROR: FAIL + format + ENDC,
        logging.CRITICAL: CRITICAL + format + ENDC,
    }

    def format(self, record):
        log_fmt = self.FORMAT.get(record.levelno)
        # Ensure the base class knows about the dynamic format
        self._style._fmt = log_fmt

        # Use the parent class to format the record
        formatted_record = super().format(record)

        # Encode to UTF-8 and then decode it. This ensures proper handling of Unicode characters
        return formatted_record.encode('utf-8').decode('utf-8')


logPath = "./Logs"

logFileName = "log.log"

fileLogformat = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

fileFormatter = logging.Formatter(fileLogformat)


fileHandler = handlers.TimedRotatingFileHandler(
    "{0}/{1}".format(logPath, logFileName), when="midnight", interval=1, backupCount=31, encoding='utf-8'
)

fileHandler.setFormatter(fileFormatter)

logging.basicConfig(format=fileLogformat, handlers=[fileHandler])


def setup_custom_logger(name):
    # formatter = logging.Formatter(CustomFormatter())

    stdout_handler = logging.StreamHandler()

    stdout_handler.setFormatter(CustomFormatter())

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)
    logger.encoding = 'utf8'

    logger.propagate = False

    logger.addHandler(stdout_handler)

    logger.addHandler(fileHandler)

    return logger
