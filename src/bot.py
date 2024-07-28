import os
import telebot

from apscheduler.schedulers.background import BackgroundScheduler
from tools import Tools
from db_connection import DBConnection
from constants import SYSTEM_MESSAGES

private_vars = os.environ
BOT_TOKEN: str = private_vars["BOT_TOKEN"]


class GreetingsBot:
    def __init__(self):
        self.__bot: telebot.TeleBot = telebot.TeleBot(BOT_TOKEN)
        self.tools: Tools = Tools()
        self.psql_connection: DBConnection = DBConnection()

        self.daily_send_hours: int = 10
        self.daily_send_minutes: int = 0
        self.daily_send_seconds: int = 0


        @self.__bot.message_handler(commands=["start"])
        def send_stat(message: telebot.types.Message) -> None:
            try:
                user_chat_id: int = message.from_user.id
                user_name: str = message.from_user.username
                if self.psql_connection.add_new_user(user_name=user_name, user_chat_id=user_chat_id):
                    self.__bot.send_message(chat_id=user_chat_id, text=SYSTEM_MESSAGES["welcome"])

                else:
                    self.__bot.send_message(chat_id=user_chat_id, text=SYSTEM_MESSAGES["user_already_exists"])

            except Exception as _ex:
                print(f"[AppealBot->send_stat]. Can't send stat message. Error :: {_ex}")


        @self.__bot.message_handler(commands=["get_audio_greeting"])
        def send_audio_greeting(message: telebot.types.Message) -> None:
            try:
                user_chat_id: int = message.from_user.id
                username: str = message.from_user.username

                self.tools.create_audio(audio_text=message.text, username=username)
                with open(f"/generated_audio/to_user_{username}.mp3", 'rb') as audio:
                    self.__bot.send_audio(user_chat_id, audio)

                os.remove(f"/generated_audio/to_user_{username}.mp3")

            except Exception as _ex:
                print(f"[AppealBot->send_audio_greeting]. Can't send audio message. Error :: {_ex}")
                self.__bot.send_message(chat_id=message.from_user.id, text=SYSTEM_MESSAGES["cant_audio"])


        @self.__bot.message_handler(commands=["get_text_greeting"])
        def send_stat(message: telebot.types.Message) -> None:
            greeting: str = self.tools.create_greeting()
            user_chat_id: int = message.from_user.id
            self.__bot.send_message(chat_id=user_chat_id, text=greeting)


        @self.__bot.message_handler(commands=["get_grandma_postcard"])
        def send_grandma_postcard(message: telebot.types.Message) -> None:
            try:
                user_chat_id: int = message.from_user.id
                postcard_filename: str = self.tools.download_image_yadisk(image_type="morning")
                photo = open(postcard_filename, "rb")
                self.__bot.send_photo(chat_id=user_chat_id, photo=photo)
                os.remove(postcard_filename)

            except Exception as _ex:
                print(f"[AppealBot->send_grandma_postcard]. Can't send postcard. Error :: {_ex}")
                self.__bot.send_message(chat_id=message.from_user.id, text=SYSTEM_MESSAGES["cant_audio"])

    def run(self):
        print(f"<== GreetingsBot has been planted ==>")
        while True:
            try:
                self.__bot.polling()

            except Exception as _ex:
                print(f"[GreetingsBot->run]. Something goes wrong. Error :: {_ex}")
                print(f"<== GreetingsBot has been replanted ==>")
