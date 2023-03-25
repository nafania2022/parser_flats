import db.db_client
import logging 
import asyncio

def answer_price_meter(sity):
    answer_price = 0
    filter_sity = db.db_client.get_filter_flats_city(sity)
    for price in filter_sity:
        answer_price += price[3]
    return  answer_price / len(filter_sity)



async def delete_message(msg, time= 0):
    await asyncio.sleep(time)
    try:
        await msg.delete()
    except Exception:
        logging.error(f'Сообщение уже удалено ')       
              