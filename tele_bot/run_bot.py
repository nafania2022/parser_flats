import asyncio
from aiogram import Bot, Dispatcher, F
from handlers import bot_start, filter_flats, add_subscriptions
from config import config




async def main():
    bot = Bot(token=config.api_token.get_secret_value())
    dp = Dispatcher()

    
    dp.include_routers(bot_start.router, add_subscriptions.router, filter_flats.router)
    
    # dp.message.register(filter_flats.post_flats_from_city_price, F.text.isdigit and filter_flats.Form.price  )
    
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

 
if __name__ == "__main__":
    asyncio.run(main())