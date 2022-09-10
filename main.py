from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from lyricsgenius import Genius

bot_token = "token"
bot = TeleBot(bot_token)


@bot.message_handler(content_types=["text"])
def start(message):
    if message.text == "Find songs by lyrics":
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Type your lyrics: ", reply_markup=ReplyKeyboardRemove()), find_songs
        )
    else:
        buttons_markup = ReplyKeyboardMarkup()
        buttons_markup.add("Find songs by lyrics")
        bot.send_message(message.chat.id, "Hi! Press a button to start working with me.", reply_markup=buttons_markup)


def find_songs(message):
    inline_markup = InlineKeyboardMarkup()
    inline_markup.row_width = 2
    inline_markup.add(InlineKeyboardButton("Link", callback_data="get_link"))
    lyrics = message.text
    genius_token = "RktvgwfbDpIeE80rsEd0Uk12aA-sq9UiSq_jzWVdXO4dx3pP9bNa2N-vrBfL6owT"
    genius = Genius(genius_token)
    request = genius.search_lyrics(lyrics)
    for song in request['sections'][0]['hits']:
        bot.send_message(message.chat.id,
                         f"<a href='{song['result']['url']}'>"
                         f"{song['result']['artist_names']} - {song['result']['title']}</a>",
                         reply_markup=inline_markup, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: True)
def get_link(call):
    if call.data == "get_link":
        bot.answer_callback_query(call.id, "Неверно, Верный ответ...", show_alert=True)

if __name__ == "__main__":
    bot.polling(none_stop=True)
