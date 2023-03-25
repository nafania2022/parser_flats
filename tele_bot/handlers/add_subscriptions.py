from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.text import Text
import db.db_client 
from constants import *
from config import config
from utils import *
from keyboards.all_keyboards import *
import re

class Sub(StatesGroup):
    subscriptions = State()


router = Router()

@router.callback_query(F.data.in_(LIST_SUBSCRIPTIONS))
async def subscriptions_flats(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id
                        )
    await state.update_data(subscriptions=call.data) 
    price = int(re.sub('[^0-9]', '', call.data.strip())) 
    title = re.sub('[^а-яА-ЯA-Za-z ]', '', call.data.strip())
    print(price)
    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=title,
        description=title,
        payload="city",
        provider_token=config.yookassa_token.get_secret_value(),
        currency="RUB",
        start_parameter="test",
        prices=[{
        'label':'rub',
        'amount': price*100
                }] )
    
    
@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)
    
    
@router.message(F.successful_payment)
async def syccessful_subscription(message: Message, state: FSMContext, bot: Bot): 
    await bot.delete_message(
     chat_id=message.from_user.id,
     message_id=message.message_id
    )
    user_subscriptions = [x[0] for x in db.db_client.get_user_id_subscriotions()]
    subscriptions = await state.get_data()
    if message.from_user. id not in user_subscriptions:
        if subscriptions['subscriptions'] == LIST_SUBSCRIPTIONS[0]:
            db.db_client.add_user_subscriptions(message.from_user.id, True, False)
        elif subscriptions['subscriptions'] == LIST_SUBSCRIPTIONS[1]:
            db.db_client.add_user_subscriptions(message.from_user.id, False, True)
        elif subscriptions['subscriptions'] == LIST_SUBSCRIPTIONS[2]:
            db.db_client.add_user_subscriptions(message.from_user.id, True, True)
    else:
        db.db_client.add_user_subscriptions(message.from_user.id, True, True)
    await bot.send_message(chat_id=message.from_user.id, text=f"Подписка {subscriptions['subscriptions']} оформлена")


