from aiogram import Router, Bot, F
from aiogram.filters.text import Text
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import db.db_client 
from constants import *
from config import config
from utils import *
from keyboards.all_keyboards import *



router = Router()


class Form(StatesGroup):
    price = State()
    city = State()


@router.callback_query(Text(text=LIST_FILTER[1]))
async def filter_city(call: CallbackQuery, state: FSMContext, bot: Bot ):
    await bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id
                        )
    button = menu(LIST_CITY)
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Выберите Город',
        reply_markup=button.as_markup()
                                )
    
    
    
@router.callback_query(Text(text=LIST_FILTER[0]))
async def filter_price(call: CallbackQuery, bot: Bot):
    await bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id
                        )
    msg = await bot.send_message(
        chat_id=call.from_user.id,
        text='Введите стоимость м² '
                                )
    


@router.callback_query(Form.city)
async def get_sity_in_form(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(
     chat_id=call.from_user.id,
     message_id=call.message.message_id
    )
    await state.update_data(city=call.data)
    await state.set_state(Form.price)
    msg = await bot.send_message(
        chat_id=call.from_user.id,
        text='Введите стоимость за м²!'
                        )
    await delete_message(msg, 10)
    
@router.message(F.text.isdigit and Form.price)
async def post_flats_from_city_price(message: Message, state: FSMContext, bot: Bot):
    await bot.delete_message(
     chat_id=message.from_user.id,
     message_id=message.message_id
    )
    await state.update_data(price=message.text)
    data = await state.get_data()
    flats= [flat for flat in db.db_client.get_filter_flats_city(data['city']) if flat[3] <= int(data['price'])]
    answer_price = answer_price_meter(data['city'])
    logging.info(f"Поиск по городу {data['city']} с ценой за м² {data['price']} пользователем {message.from_user.username} запущен")
    if len(flats) > 0:
        for post in flats:
            post_message = f'<b>Цена:</b> {post[2]} BYN\n'
            post_message += f'<b>Описание:</b> {post[6]}\n\n'
            post_message += '\n'.join(list(map(lambda el: el, post[8].split(',')[:6])))
            await bot.send_message(chat_id=message.from_user.id, text=post_message, parse_mode='html')
        await bot.send_message(chat_id=message.from_user.id, text=f'Средняя цена по городу {data["city"]} за м²: {answer_price}' )
        await message.delete()
        logging.info(f"Поиск по городу {data['city']} с ценой за м² {data['price']} пользователем {message.from_user.username} завершен успешно")
    else:
        await state.set_state(Form.price)
        msg = await bot.send_message(chat_id=message.from_user.id, text=f'Квартир в городе {data["city"]} с ценой за м²: {data["price"]} нет \n\n Введите другую цену' )  
        await delete_message(msg, 10)
        await message.delete()

@router.callback_query(Text(text=LIST_CITY))
async def post_flats_city(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id
                        )
    logging.info(f"Поиск по городу {call.data} запущен пользователем {call.from_user.username}")
    if call.data in LIST_CITY:
        flats = db.db_client.get_filter_flats_city(call.data)
        answer_price = answer_price_meter(call.data)
        if len(flats) > 0:
            for post in flats:
                post_message = f'<b>Цена:</b> {post[2]} BYN\n'
                post_message += f'<b>Описание:</b> {post[6]}\n\n'
                post_message += '\n'.join(list(map(lambda el: el, post[8].split(',')[:6])))
                await bot.send_message(chat_id=call.from_user.id, text=post_message, parse_mode='html')
            await bot.send_message(chat_id=call.from_user.id, text=f'Средняя цена по городу {call.data} за м²: {answer_price}' )
            logging.info(f"Поиск по городу {call.data}  пользователем {call.from_user.username} завершен успешно")
            
            
@router.message(F.text.isdigit)
async def post_flats_price(message: Message, bot: Bot):
    logging.info(f"Поиск по м² запущен пользователем {message.from_user.username}")
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
                        )
    if message.text.isdigit():
        flats = db.db_client.get_flats_less_price(message.text)
        if len(flats) > 0:
            for post in flats:
                post_message = f'<b>Цена:</b> {post[2]} BYN\n'
                post_message += f'<b>Описание:</b> {post[6]}\n\n'
                post_message += '\n'.join(list(map(lambda el: el, post[8].split(',')[:6])))
                await bot.send_message(
                    chat_id=message.from_user.id, 
                    text=post_message, 
                    parse_mode='html'
                                        )
            await message.delete()
            logging.info(f"Поиск по м² пользователем {message.from_user.username} завершен успешно")
        else:
            msg = await bot.send_message(chat_id=message.from_user.id,
            text="Квартир с данной стоимостью нет введите другую цену"
            )
            await delete_message(msg, 10)
    
    
@router.callback_query(Text(text=LIST_FILTER[2]))
async def filter_sity_flats(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(
     chat_id=call.from_user.id,
     message_id=call.message.message_id
    )
    await state.set_state(Form.city)
    button = menu(LIST_CITY)
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Выберите Город!',
        reply_markup=button.as_markup()
                                )
    
    

    
