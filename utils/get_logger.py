import logging
def get_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s, %(levelname)s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
        logging.StreamHandler()
    ])
    logger = logging.getLogger(f":__{name}__:")
    return logger