'''
@author: Alex F
'''
import telebot

class TelegramBot(telebot.TeleBot):
    def __init__(self, api_key):
        self._api_key = api_key
        self.bot = telebot.TeleBot(self._api_key, parse_mode=None)
        

    def send_message(self, msg):
        self.bot.send_message("1921878784", msg)

        
    

    