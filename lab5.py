import psycopg2
import sqlite3
import random

#Подключение к базе данных
conn = psycopg2.connect(database="RPP", user="sofapostgres", host="localhost", port=5432, password="Sofasofa77")
cur = conn.cursor()
conn.close()

def create_users_table():
    # Установка соединения с базой данных
    conn = sqlite3.connect('users.db')

    # Создание объекта курсора
    cursor = conn.cursor()

    # Создание таблицы "users"
    cursor.execute('''CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


# функция для добавления нового пользователя в таблицу "users"
def add_user(name, email):
    # Установка соединения с базой данных
    conn = sqlite3.connect('users.db')

    # Создание объекта курсора
    cursor = conn.cursor()

    # Добавление пользователя в таблицу "users"
    cursor.execute("INSERT INTO users(name, email) VALUES (?, ?)", (name, email))
    user_id = cursor.lastrowid

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

    # Возвращаем user_id
    return user_id


# функция для получения всех пользователей из таблицы "users"
def get_all():
    # Установка соединения с базой данных
    conn = sqlite3.connect('users.db')

    # Создание объекта курсора
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    all_users = cursor.fetchall()

    return all_users

# функция для получения пользователя по id из таблицы «users».
def get_one(id):
    # Установка соединения с базой данных
    conn = sqlite3.connect('users.db')

    # Создание объекта курсора
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    one_id = cursor.fetchone()

    return one_id

# функция для удаления пользователя по id из таблицы "users"
def delete_user_by_id(id):
    # Установка соединения с базой данных
    conn = sqlite3.connect('users.db')

    # Создание объекта курсора
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=?", (id,))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


# Создание таблицы "users"
# create_users_table()

# добавление нового пользователя
user_id = add_user("Кирилл", "kirill@mail.com")
print(f"Добавлен пользователь с id {user_id}")

# получение всех пользователей из таблицы
all_users = get_all()
print("Все пользователи:")
for user in all_users:
    print(user)

# получение пользователя по id
user = get_one(user_id)
print(f"Пользователь с id {user_id}: {user}")

# удалить пользователя по id
delete_user_by_id(6)




import sqlite3


def create_users_table():
    # Установка соединения с базой данных
    conn = sqlite3.connect('users.db')

    # Создание объекта курсора
    cursor = conn.cursor()

    # Создание таблицы "users"
    cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


# функция для добавления нового пользователя в таблицу "users"
def add_user(id, name, email):
    # Установка соединения с базой данных
    conn = sqlite3.connect('users.db')

    # Создание объекта курсора
    cursor = conn.cursor()

    # Добавление пользователя в таблицу "users"
    cursor.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)", (id, name, email))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


# функция для получения всех пользователей из таблицы "users"
def get_all_users():
    # Установка соединения с базой данных
    conn = sqlite3.connect('users.db')

    # Создание объекта курсора
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()

    # закрытие соединения
    conn.close()

    return all_users


# функция для получения пользователя по id из таблицы "users"
def get_user_by_id(user_id):
    # Установка соединения с базой данных
    conn = sqlite3.connect('users.db')

    # Создание объекта курсора
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    # закрытие соединения
    conn.close()

    return user


# функция для удаления пользователя по id из таблицы "users"
def delete_user_by_id(user_id):
    # Установка соединения с базой данных
    conn = sqlite3.connect('users.db')

    # Создание объекта курсора
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


import random


def main():
    # Создание таблицы "users"
    # create_users_table()

    # Добавление нового пользователя
    id = random.randint(1, 1000)
    name = "Ivan Ivanov"
    email = "ivanivanov@mail.com"
    add_user(id, name, email)
    print(f"Добавлен пользователь {id, name, email}")

    # Получение всех пользователей
    print("Все пользователи:")
    all_users = get_all_users()
    for user in all_users:
        print(user)

    # Получение пользователя по id
    user_id = id
    get_one = get_user_by_id(user_id)
    print(f"Добавлен пользователь с id {user_id}: {name, email}")

    # Удаление пользователя по id
    delete_user_by_id(user_id)
    print(f"Пользователь с id {user_id} удален")


if __name__ == "__main__":
    main()