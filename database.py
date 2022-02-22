import sqlite3
import datetime
import os
import psycopg2
from config import host, user, db_name, port, password
import pymongo


def get_all_unique_user_id(**kwargs):
    try:
        connect = psycopg2.connect(
                host=host,
                user=user,
                database=db_name,
                port=port,
                password=password
        )

        with connect.cursor() as cursor:
            cursor.execute(
                """
                SELECT user_id from unique_users;
                """
            )
            user_id_list = cursor.fetchall()
            try:
                if connect:
                    connect.close()
                    print("[INFO] PostgreSQL connection closed")
            except Exception as e:
                print("[INFO] Error in finally block add_new_unique_users", e)

            return user_id_list
    except Exception as e:
        print(f"[INFO] Error while connnect to Postgre database. Exception: {e}")
        return 0


def check_exist_status_user_id(user_id: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            database=db_name,
            port=port,
            password=password
        )
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT user_id FROM unique_users;
            """)
            exist_status = False
            for id in cursor.fetchall(): # [(596834788,), (123456789,)]
                if int(id[0]) == user_id:
                    exist_status = True
                    break
            return exist_status
    except Exception as e:
        print("[INFO] Error while checking exist status user_id", e)


def check_exist_status_user(db_name, table_name, user_id, coloumn_name="user_id"):
    connect = sqlite3.connect(os.path.join(os.getcwd(), db_name))
    connect.cursor()
    connect.commit()

    rows = connect.execute(f"SELECT {coloumn_name} FROM {table_name}").fetchall()
    connect.close()
    exist_status = False
    for row in rows:
        if user_id in row:
            exist_status = True
            return exist_status
    return exist_status


def save_unique_users(date, user_id, user_name):
    connect = sqlite3.connect("english_words.db")

    connect.cursor()

    connect.execute("""
    CREATE TABLE IF NOT EXISTS unique_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date VARCHAR(50) NOT NULL,
    user_id INTEGER NOT NULL,
    user_name VARCHAR(255)
    );
    """)

    connect.commit()

    connect.execute(f"INSERT INTO unique_users (date, user_id, user_name) VALUES(?, ?, ?);", (date, user_id, user_name))

    connect.commit()
    connect.close()


def insert_to_db(word, translate, example, user_id, username):
    connect = sqlite3.connect("english_words.db")

    connect.cursor()

    connect.execute("""
    CREATE TABLE IF NOT EXISTS english_words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    word TEXT NOT NULL,
    translate TEXT NOT NULL,
    example TEXT,
    user_id TEXT,
    username TEXT
    );
    """)

    connect.commit()

    date_ = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")

    connect.execute("INSERT INTO english_words (date, word, translate, example, user_id, username) VALUES(?, ?, ?, ?, ?, ?);", (date_, word, translate, example, user_id, username))

    connect.commit()
    connect.close()


def get_all_items_from_db(db_name, table_name):
    connect = sqlite3.connect(os.path.join(os.getcwd(), db_name))
    connect.cursor()
    connect.commit()

    rows = connect.execute(f"SELECT * FROM {table_name}").fetchall()
    connect.close()
    return rows


def check_exist_status_for_word(word, db_name, table_name):
    connect = sqlite3.connect(os.path.join(os.getcwd(), db_name))
    connect.cursor()
    connect.commit()

    rows = connect.execute(f"SELECT * FROM {table_name}").fetchall()
    connect.close()
    exist_status = False
    for row in rows:
        if word.lower() in row[2].lower():
            exist_status = True
            return exist_status
    return exist_status


def get_specific_word_from_db(word, db_name, table_name):
    connect = sqlite3.connect(os.path.join(os.getcwd(), db_name))
    connect.cursor()
    connect.commit()

    rows = connect.execute(f"SELECT * FROM {table_name} WHERE word = '{word}'").fetchall()
    connect.close()
    return rows


def delete_specific_word(word, db_name, table_name):
    """delete with english word"""
    connect = sqlite3.connect(os.path.join(os.getcwd(), db_name))
    connect.cursor()
    connect.commit()

    connect.execute(f"DELETE FROM {table_name} WHERE word = '{word}'")
    connect.commit()
    connect.close()


def add_column_to_table(column_name, db_name, table_name):
    connect = sqlite3.connect(os.path.join(os.getcwd(), db_name))
    connect.cursor()
    connect.commit()

    connect.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} TEXT")
    connect.commit()
    connect.close()


def get_user_send_words_allow_status():
    connect = sqlite3.connect(os.path.join(os.getcwd(), "english_words.db"))
    connect.cursor()
    connect.commit()

    all_users = connect.execute(f"SELECT * FROM send_word_allow_status").fetchall()
    return all_users


def change_user_send_word_allow_status(user_id, allow_status):
    connect = sqlite3.connect(os.path.join(os.getcwd(), "english_words.db"))
    connect.cursor()

    connect.commit()

    connect.execute(f"UPDATE send_word_allow_status SET allow_status=? WHERE user_id={user_id}", (allow_status,))
    connect.commit()
    connect.close()


def create_user_and_status_table():
    connect = sqlite3.connect(os.path.join(os.getcwd(), "english_words.db"))
    connect.cursor()

    connect.execute("""
    CREATE TABLE IF NOT EXISTS send_word_allow_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    chat_id INTEGER,
    user_fullname VARCHAR(240),
    allow_status VARCHAR(240)
    );
    """)

    connect.commit()
    connect.close()


def set_user_send_word_allow_status(user_id, user_fullname):
    connect = sqlite3.connect("english_words.db")
    connect.cursor()

    connect.execute(f"INSERT INTO send_word_allow_status (user_id, user_fullname, allow_status) VALUES(?, ?, ?);", (user_id, user_fullname, "yes"))
    connect.commit()
    connect.close()


def pymongo_client():
    # connect
    conn_string = os.getenv("URI_MONGO")
    db_client = pymongo.MongoClient(conn_string)

    return db_client


def connect_to_mongo_db(db_client, db_name: str):
    # create or connect to database
    current_db = db_client[db_name]

    return current_db


def connect_to_mongo_atlas_and_to_main_db(current_db):
    # create or connect to collection(table)
    collection = current_db["man_eng_users"]

    return collection


def connect_to_words_collection(current_db, user_id: int):
    # create or connect to collection(table)
    collection = current_db[f"user_words_{user_id}"]

    return collection
