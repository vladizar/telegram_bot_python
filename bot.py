import telebot
import weather
import similar_celebrities

from PIL import Image
from telebot import types
from random import randint

# The Message object also has a content_typeattribute, which defines the type of the Message. content_type can be one of the following strings: text, audio, document, photo, sticker, video, video_note, voice, location, contact, new_chat_members, left_chat_member, new_chat_title, new_chat_photo, delete_chat_photo, group_chat_created, supergroup_chat_created, channel_chat_created, migrate_to_chat_id, migrate_from_chat_id, pinned_message.

API_TOKEN        = "your_telegram_api_token"
STICKERS_FOLDER  = "#static/stickers"
DOWNLOADS_FOLDER = "#static/downloads"

RANDOM_BTN_TXT    = "🎲 Быстрый Рандом"
WEATHER_BTN_TXT   = "☀️ Погода"
REPEATER_BTN_TXT  = "🗣 Повторяла"
CELEBRITY_BTN_TXT = "🤩 Знаменитость"

shown_celebrities_num = None

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=["start", "help"])
def start_chat(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1   = types.KeyboardButton(RANDOM_BTN_TXT)
    btn2   = types.KeyboardButton(WEATHER_BTN_TXT)
    btn3   = types.KeyboardButton(REPEATER_BTN_TXT)
    btn4   = types.KeyboardButton(CELEBRITY_BTN_TXT)
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(msg.chat.id, f"Хай, {msg.from_user.first_name} {msg.from_user.last_name}!!!\nТебя приветствует твой же бот, если ты Vlad Zarytskyi", reply_markup=markup)

    with open(f"{STICKERS_FOLDER}/cat.webp", "rb") as sticker:
        bot.send_sticker(msg.chat.id, sticker)

    with open(f"{STICKERS_FOLDER}/meow.webp", "rb") as sticker:
        bot.send_sticker(msg.chat.id, sticker)

    bot.send_message(msg.chat.id, f"А если нет, то ты все равно топчик!😉")

@bot.message_handler(content_types=["text"])
def reply_text(msg):
    if msg.chat.type == "private":
        if msg.text == RANDOM_BTN_TXT:
            bot.reply_to(msg, f"Вам выпала цифра {randint(1, 6)}")
        elif msg.text == WEATHER_BTN_TXT:
            bot.reply_to(msg, "В каком городе узнать для вас погоду? 🧐")
            bot.register_next_step_handler(msg, send_weather)
        elif msg.text == REPEATER_BTN_TXT:
            markup = types.InlineKeyboardMarkup()
            btn1   = types.InlineKeyboardButton("🤬 Давай помолчим!!!", callback_data="silence")
            markup.add(btn1)
            bot.reply_to(msg, "Теперь я птица говорун, сам знаешь чем отличаюсь!\nА еще теперь я буду повторять каждое твое слово пока Енергия Вселенной не Исчерпается (ну или ты нажмешь на нужную кнопочку 😀)", reply_markup=markup)
            bot.register_next_step_handler(msg, repeater_mode)
        elif msg.text == CELEBRITY_BTN_TXT:
            bot.reply_to(msg, "Сколько похожих знаменитостей вы хотите увидеть?")
            bot.register_next_step_handler(msg, celebrities_num)
        else:
            bot.reply_to(msg, "Мне не рассказали как на это отвечать 🙄.\nХнык-хнык😭")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "silence":
        bot.send_message(call.message.chat.id, "Я внезапно потерял возможность повторять за тобой\nХнык-хнык😭")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text, reply_markup=None)
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

def repeater_mode(msg):
    markup = types.InlineKeyboardMarkup()
    btn1   = types.InlineKeyboardButton("🤬 Давай помолчим!!!", callback_data="silence")
    markup.add(btn1)
    bot.reply_to(msg, f"{msg.text}", reply_markup=markup)
    bot.register_next_step_handler(msg, repeater_mode)

def send_weather(msg):
    try:
        bot.reply_to(msg, f"{weather.get_weather(msg.text)}\nОбращайтесь еще 🤗")
    except Exception:
        bot.reply_to(msg, "Я не знаю такого города 🤔\nПопробуйте другой 😇")

def celebrities_num(msg):
    try:
        global shown_celebrities_num
        shown_celebrities_num = int(msg.text)
    except Exception:
        bot.reply_to(msg, "Количество знаменитостей должно быть цифрой...")
        return None

    if 0 < shown_celebrities_num < 210:
        bot.reply_to(msg, "Ок.😉 Теперь отправьте мне ваше 🖼фото, и я скажу на кого из ✨знаменитостей✨ вы похожи больше всего")
        bot.register_next_step_handler(msg, find_celebrities)
    else:
        bot.reply_to(msg, "Количество знаменитостей должно быть больше чем 1 и меньше 211...")

def find_celebrities(msg):
    if msg.content_type == "photo":
        photo_index = len(msg.photo) - 1
        photo_info  = bot.get_file(msg.photo[photo_index].file_id)

        photo = bot.download_file(photo_info.file_path)

        with open(f"{DOWNLOADS_FOLDER}/{msg.photo[photo_index].file_id}.jpg", "wb") as new_photo:
            new_photo.write(photo)

        with open("#ppl/normal/0.jpg", "wb") as new_photo:
            new_photo.write(photo)

        celebrities = similar_celebrities.get_similar_celebrities(shown_celebrities_num)

        if celebrities:
            for i, person in enumerate(celebrities):
                photo_caption = f"{shown_celebrities_num - i}. {person['name']}.\nОчки схожести: {round(1000 - person['distance'] * 1000)} из 1000\n"
                if person["distance"] < 0.46:
                    photo_caption += f"Вы и {person['name']} - один и тот же человек! Я вас расскусил)"
                elif person["distance"] < 0.56:
                    photo_caption += f"Одно лицо!!!"
                elif person["distance"] < 0.61:
                    photo_caption += f"Вы оооочень похожи!!"
                elif person["distance"] < 0.66:
                    photo_caption += f"Вы похожи!"
                elif person["distance"] < 0.76:
                    photo_caption += f"Вы чуть-чуть похожи..."
                elif person["distance"] < 0.86:
                    photo_caption += f"Вы не совсем похожи!"
                else:
                    photo_caption += f"Вы почти не похожи!!"

                with open(person["image"], "rb") as photo:
                    try:
                        bot.send_photo(msg.chat.id, photo, photo_caption)
                    except Exception:
                        bot.send_message(msg.chat.id, f"{photo_caption}\n🤖Бот не может отправлять файлы больше 💾10мб, хоть и попытался 😀\n✍️Напишите, пожалуйста, 👨🏻‍💻@vladizar123👨🏻‍💻, что бы посмотрел 🖼фото #{person['image'].split('/')[-1].split('.')[0].strip('picture')}")
        else:
            bot.reply_to(msg, f"Извините, если обидел 🙂\nЯ не нашел на этом фото лица. Совсем. Никакого. 🧐🤔")
    else:
        bot.reply_to(msg, "Мой 🖥компьютерный 🤓разум подсказал мне, что это не картинка...\nЗачем вы так со мной? 😢")

bot.polling()