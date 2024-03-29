import logging
import os
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# Объект бота
bot = Bot(token=bot_token)
# Диспетчер для бота
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

saved_data = {}

#class Context(StatesGroup):
#    currency = State()
#    number = State()


# Форма, которая хранит информацию о пользователе
class Form(StatesGroup):
    currency = State()
    number = State()


class Form2(StatesGroup):
    other_currency = State()
    sum = State()

#Сохрание данных значения
@dp.message_handler(commands=['save_currency'])
async def process_command1(message: Message):
    await Form.currency.set()
    await message.reply("Введите название валюты")


@dp.message_handler(state=Form.currency)
async def process_currency1(message: types.Message, state: FSMContext):
    print(message.text)
    await state.update_data(currency=message.text)
    await state.get_data()
    await Form.number.set()
    await message.reply("Введите курс валюты к рублю")


@dp.message_handler(state=Form.number)
async def process_currency2(message: types.Message, state: FSMContext):
    global saved_data
    print(message.text)
    await state.update_data(number=message.text)
    saved_data = await state.get_data()
    await state.finish()
    await message.reply("Курс валюты сохранен")


@dp.message_handler(commands=['convert'])
async def procces_command2(message: types.Message):
    #logging.log(f"Bot transfers to convert state after {message.text}")
    await Form2.other_currency.set()
    await message.reply("Введите название валюты")


@dp.message_handler(state=Form2.other_currency)
async def process_other_currency(message: types.Message, state: FSMContext):
    await state.update_data(other_currency=message.text)
    await state.get_data()
    await Form2.sum.set()
    await message.reply("Сумма валюты")


@dp.message_handler(state=Form2.sum)
async def process_sum(message: types.Message, state: FSMContext):
    await state.update_data(sum=message.text)
    data = await state.get_data()
    print(data)
    print(saved_data)
    if saved_data('currency')== state.get_data('other_ccurrency'):
        await message.reply(f"Сконвертированная по курсу сумма = {int(data['sum']) * int(saved_data['number'])}")
    else:
        await message.reply("Такой валюты нет")


#Точка входа в приложение
if __name__ == "__main__":
    #Инициализация системы логирования
    logging.basicConfig(level=logging.INFO)
    #Подключение системы логирования к боту
    dp.middleware.setup(LoggingMiddleware())
    #Запуск бота
    executor.start_polling(dp, skip_updates= True)