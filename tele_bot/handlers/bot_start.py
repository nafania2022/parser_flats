from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import db.db_client
from constants import *
from tele_bot.config import config
from tele_bot.keyboards.all_keyboards import *
from utils import *


router = Router()


@router.message(Command("start"))
async def start(message: Message, bot: Bot):
    user_subscriptions = [x[0] for x in db.db_client.get_user_id_subscriotions()]
    if message.from_user.id in user_subscriptions:
        subscriptions_type = db.db_client.get_subscriotions_user(message.from_user.id)[0]   
        if subscriptions_type[0] and not subscriptions_type[1]:
            button = menu([LIST_FILTER[0], LIST_FILTER[-1]])
            await bot.send_message(chat_id=message.from_user.id,
                                        text='Выберите способ сортировки',
                                        reply_markup=button.as_markup())
            await message.delete()
            
        elif subscriptions_type[1] and not subscriptions_type[0]:
            button = menu([LIST_FILTER[1], LIST_FILTER[-1]])
            await bot.send_message(chat_id=message.from_user.id,
                                        text='Выберите способ сортировки',
                                        reply_markup=button.as_markup())
            await message.delete()
            
        elif subscriptions_type[0] and subscriptions_type[1]:
            button = menu(LIST_FILTER[:-1])
            await bot.send_message(chat_id=message.from_user.id,
                                        text='Выберите способ сортировки',
                                        reply_markup=button.as_markup())
            await message.delete()
    else:
        button = menu(LIST_FILTER[-1])
        await bot.send_message(chat_id=message.from_user.id,
                                     text='Добавьте подписку',
                                     reply_markup=button.as_markup())
        await message.delete()
        
        
@router.callback_query(F.data == LIST_FILTER[-1])
async def select_subscriptions(call: CallbackQuery, bot: Bot):
    user_subscriptions = [x[0] for x in db.db_client.get_user_id_subscriotions()]
    if call.from_user.id in user_subscriptions:
        subscriptions_type = db.db_client.get_subscriotions_user(call.from_user.id)[0]
        print(subscriptions_type)
        if subscriptions_type[0] and not subscriptions_type[1]:
            button = menu(LIST_SUBSCRIPTIONS[:1])
            await bot.send_message(chat_id=call.from_user.id,
                                            text='Добавьте подписку',
                                            reply_markup=button.as_markup())
        elif subscriptions_type[1] and not subscriptions_type[0]:
            button = menu(LIST_SUBSCRIPTIONS[1:2])
            await bot.send_message(chat_id=call.from_user.id,
                                            text='Добавьте подписку',
                                            reply_markup=button.as_markup())
    else:
        button = menu(LIST_SUBSCRIPTIONS[0])
        await bot.send_message(chat_id=call.from_user.id,
                                            text='Выберите подписку',
                                            reply_markup=button.as_markup())  
        

