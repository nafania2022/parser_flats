
from parsers.realt_parser import RealtParser
import db.db_client

realt_parser = RealtParser()
USED_PARSERS = [realt_parser]
LIST_SUBSCRIPTIONS = ["По городу цена: 500 в месяц", "По стоимости м² цена: 500 в месяц", "Обе подписки цена: 800 в месяц"]
LIST_FILTER = ["По стоимости м²","По городу", "По городу и стоимости м²", "Добавить подписку " ]
LIST_CITY = [sity[0] for sity in db.db_client.get_city()]
