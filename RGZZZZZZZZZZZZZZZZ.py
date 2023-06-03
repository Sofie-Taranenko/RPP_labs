import requests
import json
import logging
import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import os
from aiogram.utils import executor
import asyncio
import datetime

api_key = "QQBTELNEZXXAENQ3"

logging.basicConfig(level=logging.INFO)

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="Sofasofa44",
    port="5432"
)


cursor = conn.cursor()
create_table_query = '''
CREATE TABLE IF NOT EXISTS stocks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    stock_name VARCHAR(255)
);'''

create_table = '''CREATE TABLE IF NOT EXISTS performance (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    portfolio_performance FLOAT,
    calculation_date DATE
);
'''

cursor.execute(create_table_query)
cursor.execute(create_table)
conn.commit()

cursor = conn.cursor()
select_query = 'SELECT * FROM performance;'
cursor.execute(select_query)
result = cursor.fetchall()

for row in result:
    print(row)


PERFORMANCE_CALCULATION_INTERVAL = datetime.timedelta(days=1)


async def set_bot_commands():
    commands = [
        types.BotCommand(command="/start", description="Запуск бота"),
        types.BotCommand(command="/performance", description="Показать производительность портфеля"),
        types.BotCommand(command="/show_all", description="Показать все бумаги"),
        types.BotCommand(command="/delete", description="Удалить бумагу"),
    ]

    await bot.set_my_commands(commands, scope=types.BotCommandScopeDefault())



loop = asyncio.get_event_loop()
loop.run_until_complete(set_bot_commands())


class AddPaperState(StatesGroup):
    waiting_for_stock_name = State()


class DeletePaperState(StatesGroup):
    waiting_for_stock_name = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Добавить ценную бумагу к портфелю", callback_data="add_stock")
    keyboard.add(button)

    await message.reply("Привет! Я бот для конвертации валют.", reply_markup=keyboard)


@dp.callback_query_handler(text="add_stock")
async def add_stock_callback(query: types.CallbackQuery):
    await query.answer()
    await query.message.answer('Введите имя ценной бумаги:')
    await AddPaperState.waiting_for_stock_name.set()


@dp.message_handler(text='Добавить ценную бумагу к портфелю')
async def add_stock_handler(message: types.Message):
    await message.answer('Введите имя ценной бумаги:')
    await AddPaperState.waiting_for_stock_name.set()


def check_stock_exists(stock_name):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={stock_name}&apikey={api_key}"
    response = requests.get(url)
    data = json.loads(response.text)

    if 'bestMatches' in data and len(data['bestMatches']) > 0:
        return True

    return False


@dp.message_handler(state=AddPaperState.waiting_for_stock_name)
async def process_stock_name(message: types.Message, state: FSMContext):
    stock_name = message.text

    if not check_stock_exists(stock_name):
        await message.answer('Ценная бумага не найдена. Пожалуйста, убедитесь, что имя ценной бумаги верно.')
        return

    save_stock_to_database(message.from_user.id, stock_name)
    await message.answer(f'Ценная бумага {stock_name} добавлена к отслеживаемым')
    await state.finish()


@dp.message_handler(commands=['performance'])
async def show_performance_handler(message: types.Message):
    stocks = get_tracked_stocks(message.from_user.id)

    if not stocks:
        await message.answer('Вы не отслеживаете ни одной ценной бумаги')
    else:
        portfolio_performance = calculate_portfolio_performance(stocks)
        save_performance_to_database(message.from_user.id, portfolio_performance)
        await message.answer(f'Индекс производительности портфеля:\n{portfolio_performance}')


@dp.message_handler(commands=['show_all'])
async def show_all_stocks_handler(message: types.Message):
    stocks = get_tracked_stocks(message.from_user.id)

    if not stocks:
        await message.answer('Ценные бумаги не найдены')
    else:
        formatted_stocks = '\n'.join(stocks)
        await message.answer(f'Сохраненные ценные бумаги:\n{formatted_stocks}')


@dp.message_handler(commands=['delete'])
async def delete_stock_handler(message: types.Message):
    stocks = get_tracked_stocks(message.from_user.id)

    if not stocks:
        await message.answer('У вас нет сохраненных ценных бумаг для удаления')
    else:
        formatted_stocks = '\n'.join(stocks)
        await message.answer(f'Выберите ценную бумагу для удаления:\n{formatted_stocks}')
        await DeletePaperState.waiting_for_stock_name.set()


@dp.message_handler(state=DeletePaperState.waiting_for_stock_name)
async def delete_stock_name(message: types.Message, state: FSMContext):
    stock_name = message.text

    delete_stock_from_database(message.from_user.id, stock_name)
    await message.answer(f'Ценная бумага {stock_name} удалена из отслеживаемых')
    await state.finish()


def get_tracked_stocks(user_id: int):
    cursor = conn.cursor()
    cursor.execute('SELECT stock_name FROM stocks WHERE user_id = %s', (user_id,))
    stocks = cursor.fetchall()
    cursor.close()

    return [stock[0] for stock in stocks]


def calculate_portfolio_performance(stocks):
    start_prices = []
    end_prices = []

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=30)

    for stock in stocks:
        symbol = stock
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" \
              f"{symbol}&outputsize=full&apikey={api_key}"
        response = requests.get(url)
        data = json.loads(response.text)

        time_series = data['Time Series (Daily)']
        closing_prices = []
        for date, values in time_series.items():
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if start_date <= date <= end_date:
                closing_price = float(values['4. close'])
                closing_prices.append(closing_price)

        start_prices.append(closing_prices[0])
        end_prices.append(closing_prices[-1])

    start_portfolio_value = sum(start_prices)
    end_portfolio_value = sum(end_prices)

    performance = (end_portfolio_value - start_portfolio_value) / start_portfolio_value * 100
    return round(performance, 4)


def save_stock_to_database(user_id, stock_name):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO stocks (user_id, stock_name) VALUES (%s, %s)', (user_id, stock_name))
    conn.commit()
    cursor.close()


def delete_stock_from_database(user_id, stock_name):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM stocks WHERE user_id = %s AND stock_name = %s', (user_id, stock_name))
    conn.commit()
    cursor.close()


def save_performance_to_database(user_id, portfolio_performance):
    today = datetime.date.today()

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM performance WHERE user_id = %s AND calculation_date = %s', (user_id, today))
    existing_data = cursor.fetchall()

    if existing_data:
        cursor.execute('UPDATE performance SET portfolio_performance = %s WHERE user_id = %s AND calculation_date = %s',
                       (portfolio_performance, user_id, today))
    else:
        cursor.execute('INSERT INTO performance (user_id, portfolio_performance, calculation_date) VALUES (%s, %s, %s)',
                       (user_id, portfolio_performance, today))

    conn.commit()
    cursor.close()


async def calculate_and_save_performance():
    while True:
        users = get_all_users()
        for user in users:
            stocks = get_tracked_stocks(user)
            if stocks:
                portfolio_performance = calculate_portfolio_performance(stocks)
                save_performance_to_database(user, portfolio_performance)

        await asyncio.sleep(PERFORMANCE_CALCULATION_INTERVAL.total_seconds())


def get_all_users():
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT user_id FROM stocks')
    users = cursor.fetchall()
    cursor.close()

    return [user[0] for user in users]


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(calculate_and_save_performance())
    executor.start_polling(dp, skip_updates=True)
