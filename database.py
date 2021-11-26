import sqlite3
import datetime
import os


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