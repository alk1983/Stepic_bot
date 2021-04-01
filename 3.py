import requests
import redis
import os
import json
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


redis_url = os.environ.get('REDIS_URL')
dict_ob = {}
def load_(key):
    if redis_url:
        redis_ob = redis.from_url(redis_url)
        return redis_ob.get(key)
    else:
        return dict_ob.get(key)

print(load_(123))

#save('k{0}'.format(user_id), json.dumps(k))
#save('k', json.dumps(k))
redis_ob = redis.from_url(redis_url)
dict_ob = json.load(open('data.json', 'r', encoding= 'utf-8'))
dict_ob_url = json.loads(redis_ob.get('data'))
a = '56.89 34l45'
if (a.split()[0]).isalpha() or (a.split()[1]).isalpha():
    print(a.split()[0])
print(a.split()[1])
#print(json.loads(dict_ob["k1190926674"])[0])
print(dict_ob_url)
db_url = os.environ.get('DATABASE_URL')

'''
try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(
                                  # пароль, который указали при установке Postgre
                                  DATABASE_URL, sslmode='require')
    # Создайте курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # SQL-запрос для создания новой таблицы
    create_table_query = ''CREATE TABLE bot
                             (ID VARCHAR PRIMARY KEY     NOT NULL,
                             STATE           TEXT    NOT NULL,
                             KLAT         REAL,
                             KLON         REAL,
                             IP           TEXT); ''
    # Выполнение команды: это создает новую таблицу
    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица успешно создана в PostgreSQL")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
'''
def save_state(user_id, state):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            db_url, sslmode='require')
        # Создайте курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        postgresql_select_query = "select * from bot where id = %s"

        cursor.execute(postgresql_select_query, (user_id,))
        if len(cursor.fetchall()) == 0:
            insert_query = """ INSERT INTO bot (ID, STATE) VALUES (%s, %s)"""
            cursor.execute(insert_query, (user_id,state,))
        else:
            update_query = """Update bot set STATE = %s where id = %s"""
            cursor.execute(update_query, (state, user_id,))
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def load (user_id, index):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            db_url, sslmode='require')
        # Создайте курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        postgresql_select_query = "select * from bot where id = %s"

        cursor.execute(postgresql_select_query, (user_id,))
        bot_data = cursor.fetchall()
        for row in bot_data:
            return row[index]

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
def save_k(user_id, k):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            db_url, sslmode='require')
        # Создайте курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        postgresql_select_query = "select * from bot where id = %s"
        cursor.execute(postgresql_select_query, (user_id,))


        update_query = """Update bot set KLAT = %s where id = %s"""
        cursor.execute(update_query, (k[user_id][-2], user_id,))
        update_query = """Update bot set KLON = %s where id = %s"""
        cursor.execute(update_query, (k[user_id][-1], user_id,))
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
k={'1190926674':[52.1368, 29.3813, 53.89, 27.55]

}
save_state('1190926674', 'main')
save_k('1190926674', k)
print(load('1190926674',2))