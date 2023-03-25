import schedule
import time
from constants import USED_PARSERS
import db.db_client
import sentry.sentry_logger as sentry_logger
import logging

TIME = "00:00"

def update_is_archive():
    logging.info("Проверка квартир и подписок стартовала")
    links = USED_PARSERS[0].get_all_last_flats_links(1, 'last')
    all_is_archive = db.db_client.get_flats_not_archive(links)
    db.db_client.update_is_archive_state(list(map(lambda el: el[9], all_is_archive)))
    db.db_client.check_subscriptions()
    logging.info("Проверка квартир и подписок успешно завершилась")

schedule.every().day.at(TIME).do(update_is_archive)


while True:
    schedule.run_pending()
    time.sleep(1)
