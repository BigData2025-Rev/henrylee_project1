import logging

def get_logger():
    # Configure the logger
    logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

    # Creating an object
    logger = logging.getLogger()

    return logger