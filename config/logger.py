import logging



class MaxLevelFilter(logging.Filter):

    def __init__(self, level):

        self.level = level

    def filter(self, record):

        return record.levelno < self.level



logger = logging.getLogger()

logger.setLevel(logging.INFO)



normal_handler = logging.FileHandler(
    "final_output.log"
)

normal_handler.setLevel(
    logging.INFO
)


normal_handler.addFilter(
    MaxLevelFilter(logging.ERROR)
)

normal_handler.setFormatter(

    logging.Formatter(

        '%(asctime)s - %(message)s',

        datefmt='%Y-%m-%d %H:%M:%S'
    )
)




error_handler = logging.FileHandler(
    "errors.log"
)

error_handler.setLevel(
    logging.ERROR
)

error_handler.setFormatter(

    logging.Formatter(

        '%(asctime)s - %(message)s',

        datefmt='%Y-%m-%d %H:%M:%S'
    )
)




console_handler = logging.StreamHandler()

console_handler.setLevel(
    logging.INFO
)

console_handler.setFormatter(

    logging.Formatter(

        '%(asctime)s - %(message)s',

        datefmt='%Y-%m-%d %H:%M:%S'
    )
)



logger.addHandler(normal_handler)

logger.addHandler(error_handler)

logger.addHandler(console_handler)



logger = logging.getLogger(__name__)