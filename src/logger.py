import logging

def setup_logger():
    logger = logging.getLogger('WhatsAppAnalysisLogger')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('app.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# Usage example:
logger = setup_logger()
logger.info("Logger setup successfully.")
