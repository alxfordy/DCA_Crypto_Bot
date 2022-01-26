'''
@author: Alex F
'''
import telebot

class TelegramBot(telebot.TeleBot):
    def __init__(self, api_key, chat_id):
        self._api_key = api_key
        self.bot = telebot.TeleBot(self._api_key, parse_mode=None)
        self._chat_id = chat_id
        

    def send_message(self, msg):
        self.bot.send_message(self._chat_id, msg)

        
    

    