import schedule
import time
from constants import USED_PARSERS
import tele_bot.tg_poster as tg_poster
from datetime import datetime
import db.db_client
import sentry.sentry_logger as sentry_logger
import logging

PARSE_EVERY_MINUTES = 1


def do_post_in_telegram():
    logging.info("Телеграм оповещения стартовали")
    print(f'Телеграм оповещения стартовали: {datetime.now()}')
    parser_names = list(map(lambda el: el.get_parser_name(), USED_PARSERS))
    posts = db.db_client.get_all_not_posted_flats(parser_names)
    for post in posts:
        post_message = f'<b>Цена:</b> {post[2]} BYN\n'
        post_message += f'<b>Описание:</b> {post[6]}\n\n'
        post_message += '\n'.join(list(map(lambda el: el, post[8].split(',')[:6])))
        tg_poster.send_tg_post(post_message)
        time.sleep(1)
    db.db_client.update_is_posted_state(list(map(lambda el: el[9], posts)))
    logging.info("Телеграм оповещения завершино успешно")
    time.sleep(20)
    
schedule.every(PARSE_EVERY_MINUTES).minutes.do(do_post_in_telegram)


while True:
    schedule.run_pending()
    time.sleep(1)
