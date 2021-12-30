import datetime
import os
import time

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
import asyncio
from googletrans import Translator
from alphabet_detector import AlphabetDetector
import gtts
from dotenv import load_dotenv

from database import *

# import pytesseract as tess
# tess.pytesseract.tesseract_cmd = r"C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
# tess.pytesseract.tesseract_cmd = os.path.join(os.getcwd(), "Tesseract-OCR", "tesseract.exe")
# tess.pytesseract.tesseract_cmd = r"C:\Users\User\Desktop\Rasul\Python\any_projects_and_scripts\tg_bot_for_manually_english\manually_english_bot"
# from PIL import Image
import schedule
import random
# import cv2

translator = Translator(service_urls=['translate.googleapis.com'])
ad = AlphabetDetector()
load_dotenv() # it is needed if i run from localhost
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

# Buttons
# add_word_button = KeyboardButton("Add new word")
# translate_button = KeyboardButton("Translate")
# send_message_to_dev_botton = KeyboardButton("Send message to developer")
# get_all_words_button = KeyboardButton("Get all words")
# help_button = KeyboardButton("Help")
stop_button = KeyboardButton("stop")
reverse_translation = KeyboardButton("Обратный перевод")

# all_buttons = ReplyKeyboardMarkup(resize_keyboard=True).row(add_word_button, translate_button).row(get_all_words_button, help_button).row(send_message_to_dev_botton)
# # all_buttons = ReplyKeyboardMarkup(resize_keyboard=True).row(add_word_button, translate_button, send_message_to_dev_botton, get_all_words_button, help_button)
stop_button_show = ReplyKeyboardMarkup(resize_keyboard=True).add(stop_button).row(reverse_translation)


class SendMessageToDev(StatesGroup):
    hendl1 = State()


class AddWordToDatabase(StatesGroup):
    hendl1 = State()


class TranslateWord(StatesGroup):
    hendle1 = State()


class DeleteWord(StatesGroup):
    hendle1 = State()


class TransalteAndPronounce(StatesGroup):
    hendle1 = State()

class SendMessageToAllAboutUpdates(StatesGroup):
    hendle1 = State()


last_word = ""


# connect to database
users_mongo_collection = connect_to_mongo_atlas_and_to_main_db()


@dp.message_handler(commands=["start"])
async def say_hi(message: types.Message):
    await message.reply(f"Привет {message.from_user.first_name}\n\nНажми на /help")
    # if add_new_unique_users(user_name=message.from_user.full_name, user_id=message.from_user.id, bot=bot):
    #     await bot.send_message(596834788, f"NEW USER:\n\nID: {message.from_user.id}\n\nUSERNAME: @{message.from_user.username}"
    #                                       f"\n\n"
    #                                       f"USER: {message.from_user.full_name}")
    doc = {"user_name": message.from_user.full_name, "user_id": message.from_user.id, "push_start_count": 1, "added_date": datetime.datetime.utcnow()}

    query = {"user_id": message.from_user.id}
    try:
        if users_mongo_collection.find_one(query) is None:
            users_mongo_collection.insert_one(document=doc)
            await bot.send_message(596834788, f"[INFO] New user added:\n\n"
                                              f"User: {message.from_user.full_name}\n"
                                              f"ID: {message.from_user.id}")
        else:
            push_start_count = users_mongo_collection.find_one(query)["push_start_count"] + 1
            print(users_mongo_collection.update_one(filter=query, update={"$set": {"push_start_count": push_start_count}}))
    except Exception as e:
        print(f"{datetime.datetime.utcnow()} [INFO] Exception while add new user to Mongo database. Exception: {e})")

my_commands = """
    Список доступных команд:
    /start
    /translate
    /send_message_to_developer
    """
#     /send_my_words
#     /delete_word
# / add_new_word


@dp.message_handler(commands=["help"])
async def help_text(message: types.Message):
    await bot.send_message(message.from_user.id, my_commands)


@dp.message_handler(Command("send_message_to_developer"), state=None)
async def send_message_to_developer_command(message: types.Message):
    await message.reply("Напишите ваше предложение, жалобу или благодарность разработчику :)")
    # print("send_message_to_developer", message.text)

    # с помощью сет мы будем ловить ответ и сохранить состояние
    await SendMessageToDev.hendl1.set()


@dp.message_handler(state=SendMessageToDev.hendl1)
async def send_message_to_developer(message: types.Message, state: FSMContext):
    await message.answer("Ваше сообщение отправлено. Я отвечу вам, если это предложение или жалоба.\n"
                        "Если благодарность, то позвольте сказать Спасибо через это сообщение :)\n"
                        "Это для меня очень ценно!")
    text_for_dev = f"MESSAGE FROM:\n\n" \
                   f"ID: {message.from_user.id}\n\n" \
                   f"USER: {message.from_user.full_name} \n\n" \
                   f"USERNAME: @{message.from_user.username}\n\n" \
                   f"MESSAGE:\n\n" + \
                    message.text
    await bot.send_message(596834788, text_for_dev)
    await bot.send_message(message.chat.id, my_commands)
    await state.finish()


# @dp.message_handler(commands=["translate"], state=None)
# async def get_word_command(message: types.Message):
#     print("translate",message.text)
#     await message.reply("Введите текст для перевода")

#     await TranslateWord.first()


# @dp.message_handler(state=TranslateWord.hendle1)
# async def get_word_from_db(message: types.Message, state: FSMContext):
#     print("get_word_from_db", message.text)
#     if message.text == "stop":
#         await state.finish()
#         await bot.send_message(message.chat.id, "Бот вернулся в исходное состояние")
#         await bot.send_message(message.chat.id, my_commands)
#         return
#     # rows = get_specific_word_from_db(message.text, "english_words.db", "english_words")
#     # if len(rows) != 0:
#     #     await message.reply(f"{rows[0][3]}\n\n{rows[0][4]}")
#     # else:
#     #     await message.reply(f"Слово {message.text} не было добавлено")
#     # await bot.send_message(message.chat.id, my_commands)
#     if ad.only_alphabet_chars(f"{message.text}", "CYRILLIC"):
#         translated = translator.translate(text=message.text, dest="en")
#     elif ad.detect_alphabet(u'Cyrillic and кириллический') == {'CYRILLIC', 'LATIN'} and not ad.is_latin(f"{message.text}"):
#         translated = translator.translate(text=message.text, dest="en")
#     else:
#         translated = translator.translate(text=message.text, dest="ru")
#     print("first part")
#     print(translated.text)
#     print(type(translated))
#     await bot.send_message(message.chat.id, translated.text)
#     await bot.send_message(message.chat.id, "\nЧтобы выйти из режиме перевода введите слово 'stop'\nИли введите следующий текст", reply_markup=stop_button_show)


@dp.message_handler(commands=["translate"], state=None)
async def with_command_translate_and_pronounce(message: types.Message):
    await message.reply("Введите текст для перевода и произношения")
    await TransalteAndPronounce.first()


@dp.message_handler(state=TransalteAndPronounce.hendle1)
async def translate_and_pronounce(message: types.Message, state: FSMContext):
    global last_word

    if message.text == "stop":
        await state.finish()
        await bot.send_message(message.chat.id, "Бот вернулся в исходное состояние")
        await bot.send_message(message.chat.id, my_commands)
        return None

    if message.text.lower() == "обратный перевод":
        text_for_pronounce_translate = last_word
    else:
        text_for_pronounce_translate = message.text

    if ad.only_alphabet_chars(f"{text_for_pronounce_translate}", "CYRILLIC"):
        translated = translator.translate(text=text_for_pronounce_translate, dest="en")
        text_for_pronounce = translated.text
    elif ad.detect_alphabet(u'Cyrillic and кириллический') == {'CYRILLIC', 'LATIN'} and not ad.is_latin(
            f"{text_for_pronounce_translate}"):
        translated = translator.translate(text=text_for_pronounce_translate, dest="en")
        text_for_pronounce = translated.text
    else:
        translated = translator.translate(text=text_for_pronounce_translate, dest="ru")
        text_for_pronounce = text_for_pronounce_translate
    await bot.send_message(message.chat.id, translated.text)
    tts = gtts.gTTS(text_for_pronounce)
    tts.save("translate_and_pronounce.mp3")
    await bot.send_audio(message.from_user.id,
                         audio=open(os.path.join(os.getcwd(), "translate_and_pronounce.mp3"), "rb"), title=f'Озвучка {text_for_pronounce[:6]}...')
    os.remove(os.path.join(os.getcwd(), "translate_and_pronounce.mp3"))
    await bot.send_message(message.chat.id,
                           "\nЧтобы выйти из режиме перевода введите слово 'stop'\nИли введите следующий текст",
                           reply_markup=stop_button_show)

    # save last word for able reverse translation
    if message.text.lower() == "обратный перевод" or message.text.lower() == "stop":
        pass
    else:
        last_word = translated.text


@dp.message_handler(commands=["add_new_word"], state=None)
async def add_new_word_command(message: types.Message):
    await message.reply("Добавить новое слово:\n\nВведите русское слово, его перевод и пример для использования "
                        "через пробел, к примеру:\n\n"
                        "Apple Яблоко"
                        "\n\nЕсли хотите указать пример, добавьте его внутри скобок, пример:"
                        "\n\n Apple Яблоко (tasty apple - вкусное яблоко)")
    await asyncio.sleep(0.5)
    await message.reply("Введите новое слово:")
    await bot.send_message(message.chat.id, "Для отмены нажмите 'stop'", reply_markup=stop_button_show)
    await AddWordToDatabase.first()


@dp.message_handler(state=AddWordToDatabase.hendl1)
async def add_new_word_add_to_db(message: types.Message, state: FSMContext):
    example_en_ru = "no examples"
    if message.text == "stop":
        await bot.send_message(message.chat.id, "Бот вернулся в исходный режим")
        await bot.send_message(message.chat.id, my_commands)
        await state.finish()
        return

    if "(" in message.text:
        try:
            word_list = message.text.split("(")
            example_en_ru = word_list[-1].split(")")[0].strip()
            english_word = word_list[0].split("--")[0].strip()
            russian_word = word_list[0].split("--")[1].strip()
        except Exception as e:
            print("add word exception", e)
            await message.reply("Неправильный формат\n\n/add_new_word")
            await add_new_word_command(message=message)
    else:
        word_list = message.text.split("--")
        english_word = word_list[0].strip()
        russian_word = word_list[1].strip()

    exist_status = check_exist_status_for_word(english_word, "english_words.db", "english_words")
    if not exist_status:
        insert_to_db(english_word, russian_word, example_en_ru, message.from_user.id, message.from_user.full_name)
        await message.reply(f"Новое слово {english_word} успешно добавлено")
    else:
        await message.reply(f"Слово {english_word} уже добавлено")
    await bot.send_message(message.chat.id, my_commands)
    await state.finish()


# @dp.message_handler(commands=["get_all_words"])
# async def get_all_words(message: types.Message):
#     rows = get_all_items_from_db("english_words.db", "english_words")
#     date = ""
#     english_word = ""
#     ru_word = ""
#     descrip = ""
#     all_words = ""
#     for row in rows:
#         date = row[1]
#         english_word = row[2]
#         ru_word = row[3]
#         descrip = row[4]
#         if descrip != "no examples":
#             all_words += english_word + " : " + ru_word + "\n" + "Example: " + descrip + "\n\n"
#         else:
#             all_words += english_word + " : " + ru_word + "\n\n"
#         # await message.reply(f"{english_word} - {ru_word}\n\n")
#     await message.reply(all_words)
#     await message.answer(my_commands)


@dp.message_handler(commands=["delete_word"], state=None)
async def delete_word(message: types.Message):
    await bot.send_message(message.chat.id, "Напишите английское слово которое хотите удалить")
    await DeleteWord.first()


@dp.message_handler(state=DeleteWord.hendle1)
async def delete_work_state1(message: types.Message, state: FSMContext):
    if check_exist_status_for_word(message.text, "english_words.db", "english_words"):
        await message.reply(f"Слово {message.text} удалено")
        delete_specific_word(message.text, "english_words.db", "english_words")
    else:
        await message.reply("Вы ввели слово, которого нету в базе")
    await bot.send_message(message.from_user.id, my_commands)
    await state.finish()


# @dp.message_handler(content_types=['photo'])
# async def handle_docs_photo(message: types.Message):
#     await message.photo[-1].download(os.path.join(os.getcwd(), 'get_text_test.png'))
#     await bot.send_message(message.chat.id, "Идет процесс чтения файла...")
#
#     async def get_text_from_photo():
#         flag_exist_photo = False
#         print(1)
#         while not flag_exist_photo:
#             print(2)
#             all_files = [file for file in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), file))]
#             if "get_text_test.png" in all_files:
#                 flag_exist_photo = True
#             time.sleep(0.2)
#             print(3)
#         print(4)
#         image_1 = Image.open(os.path.join(os.getcwd(), "get_text_test.png"))
#         # image_1 = cv2.imread(os.path.join(os.getcwd(), "get_text_test.png"))
#         # print(5)
#         text_1 = tess.image_to_string(image=image_1, timeout=15)
#         print(6)
#         os.remove(os.path.join(os.getcwd(), "get_text_test.png"))
#         return text_1
#     text_1 = await get_text_from_photo()
#     try:
#         print(7)
#         await bot.send_message(message.chat.id, f"Текст с изображения:\n\n{text_1}")
#     except:
#         await bot.send_message(message.chat.id, f"Текст с изображения:")
#
#     translated = translator.translate(text=text_1, dest="ru")
#     await bot.send_message(message.chat.id, f"Перевод текста:\n\n{translated.text}")
#     await bot.send_message(message.chat.id, my_commands)


# @dp.message_handler(commands=["send_my_words"])
# async def send_my_words_status(message: types.Message):
#     all_users = get_user_send_words_allow_status()
#     flag_exist = False
#     for user in all_users:
#         if message.from_user.id == user[1]:
#             flag_exist = True
#             if user[4] == "yes":
#                 change_user_send_word_allow_status(user_id=message.from_user.id, allow_status="no")
#                 await bot.send_message(message.chat.id, "Вы отключили режим отправки слов")
#             else:
#                 change_user_send_word_allow_status(user_id=message.from_user.id, allow_status="yes")
#                 await bot.send_message(message.chat.id, "Вы включили режим отправки слов")
#     if flag_exist:
#         return
#     else:
#         set_user_send_word_allow_status(message.from_user.id, message.from_user.full_name)
#         await bot.send_message(message.chat.id, "Вы включили режим отправки английских слов, каждые Х минут времени."
#                                                 "Чтобы отключить нажмите на команду /send_my_words еще раз")


# async def send_random_word_in_manually_database():
#     while True:
#         all_users = get_user_send_words_allow_status()
#         rows = get_all_items_from_db("english_words.db", "english_words")
#         random_word = rows[random.randint(0, len(rows) - 1)]
#         tts = gtts.gTTS(random_word[2])
#         tts.save("send_word_audio.mp3")
#         print("i am working: ", all_users)
#         for user in all_users:
#             if user[4] == "yes":
#                 print("user_id", user[1])
#                 if random_word[4] != "no examples":
#                     await bot.send_message(user[1], f"{random_word[2]} --- {random_word[3]}\n\n{random_word[4]}\n\nЧтобы отключить отправку слов нажмите на команду /send_my_words")
#                     await bot.send_audio(user[1],
#                                          audio=open(os.path.join(os.getcwd(), "send_word_audio.mp3"), "rb"),
#                                          title='Озвучка')
#                     os.remove(os.path.join(os.getcwd(), "send_word_audio.mp3"))
#                 else:
#                     try:
#                         await bot.send_message(user[1], f"{random_word[2]} --- {random_word[3]}\n\nЧтобы отключить отправку слов нажмите на команду /send_my_words")
#                         await bot.send_audio(user[1],
#                                              audio=open(os.path.join(os.getcwd(), "send_word_audio.mp3"), "rb"),
#                                              title='Озвучка')
#                         os.remove(os.path.join(os.getcwd(), "send_word_audio.mp3"))
#                     except Exception as e:
#                         print("Exception from send_random_word", e)
#                         continue
#                 print(f"{user[3]} {'-' * 10} отправлено слово")
#         try:
#             os.remove(os.path.join(os.getcwd(), "send_word_audio.mp3"))
#             os.remove("send_word_audio.mp3")
#         except:
#             pass
#         await asyncio.sleep(600)

@dp.message_handler(commands=["about_update"], state=None)
async def about_update_command_part(message: types.Message):
    await bot.send_message(596834788, "Введите текст для отправки всем пользователям бота")
    await SendMessageToAllAboutUpdates.first()


@dp.message_handler(state=SendMessageToAllAboutUpdates.hendle1)
async def about_update_send_message(message: types.Message, state: FSMContext):
    date = datetime.datetime.today().strftime("%Y%m%d")
    id_list = get_all_unique_user_id()
    if id_list:
        for id_ in id_list:
            await bot.send_message(id_, f"Обновления: {date}\n\n{message.text}")
    await state.finish()


@dp.message_handler()
async def nothing_to_stop(message: types.Message):
    if message.text == "stop":
        await bot.send_message(message.from_user.id, "Нет процессов для остановки")
    else:
        await bot.send_message(message.from_user.id, "Я вас не понял\n\n"
                                                     "Если вы хотите перевести текст,"
                                                     "\nсначала нажмите на /translate\n\n"
                                                     "Для других команд нажмите /help")


@dp.message_handler(commands=["get_all_users"])
async def get_all_users_from_mongo_db(message: types.Message):
    global users_mongo_collection
    string = ""
    for doc in users_mongo_collection.find({}):
        string += doc["user_name"] + "\n"
        string += str(doc["user_id"]) + "\n"
        string += str(doc["push_start_count"]) + "\n"
        string += str(doc["added_date"]) + "\n\n"

    await bot.send_message(596834788, string)


def two_():
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except Exception as e:
            print(e)
            executor.start_polling(dp, skip_updates=True)


# def one_():
#     while True:
#         asyncio.run(send_random_word_in_manually_database())
