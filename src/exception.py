class CustomException(Exception):
    def __init__(self, message, logger):
        super().__init__(message)
        logger.error(message)
        self.message = message
