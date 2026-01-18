""" This is the entry point of the GCRental application """

import logging
import os
from services.auth_service import AuthService
from database.sqlite_db_handler import SQLiteDBHandler
from database.schema import SchemaHandler
from cui.main_cui import MainCUI
from configs.app_constants import DB_FILE_NAME
from repositeries.user_repositery import UserRepo

def main():
    """main script"""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("GCRental App Launched Successfully!!!")

    # if os.path.exists(DB_FILE_NAME):
    #     os.remove(DB_FILE_NAME)

    db = SQLiteDBHandler(DB_FILE_NAME)
    db.connect()
    SchemaHandler.initialise(db)

    user_repo = UserRepo(db)
    auth = AuthService(user_repo)
    MainCUI.show_home_screen(auth)

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler('gc_app.log', mode='w')
        ]
    )

if __name__ == "__main__":
    main()
