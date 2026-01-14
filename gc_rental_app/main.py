""" This is the entry point of the GCRental application """

import logging

def main():
    """main script"""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("GCRental App Launched Successfully!!!")

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler('gc_app.log', mode='w'),
            logging.StreamHandler()
        ]
    )

if __name__ == "__main__":
    main()
