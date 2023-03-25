import schedule
import time
from constants import USED_PARSERS
import threading
import db.db_client

import sentry.sentry_logger as sentry_logger
import logging



PARSE_EVERY_MINUTES = 5


def parse_all():
    for parser in USED_PARSERS:
        thread = threading.Thread(target=parser.update_with_last_flats)
        thread.start()
    db.db_client.insert_cities()
    

schedule.every(PARSE_EVERY_MINUTES).minutes.do(parse_all)

while True:
    schedule.run_pending()
    time.sleep(1)


# parse_all()