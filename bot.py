from components.BinanceDCABot import BinanceBot
from components.CoinbaseDCABot import CoinbaseBot
from components.TelegramBot import TelegramBot
from dotenv import load_dotenv
import argparse
import os
import telebot



if __name__ =="__main__":
    parser = argparse.ArgumentParser(description='Dollar Cost Averaging Bot that works on Coinbase Pro or Binance, this should be run via CRON')
    parser.add_argument('--coinbase', action="store_true",
                        help='Use the coinbase DCA', required=False)
    parser.add_argument('--binance', action="store_true",
                        help='Use the binance DCA', required=False)
    parser.add_argument('--amount', action="store", help="The amount you would like to invest e.g 10.00", required=False)
    parser.add_argument('--token', action="store", help="The token you wish to buy e.g ADA-GBP", required=False)
    parser.add_argument('--findchatid', action="store_true", help="Flag to use to find your chat ID for your bot", required=False)
    parser.add_argument('--chatid', action="store", help="If set, this will cause the bot to send you a message depending on how the trade goes", required=False)
    load_dotenv()
    args = parser.parse_args()
    if args.findchatid:
        bot = telebot.TeleBot(os.getenv("TELEGRAM_API_KEY"))
        @bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            bot.reply_to(message, f"Chat-Id {message.chat.id}")
        bot.polling()
    #argparse sets unset arguments to None
    if args.coinbase:
        cb_api_key = os.getenv('CB_API_KEY')
        cb_secret_key = os.getenv('CB_SECRET_KEY')
        cb_passphrase = os.getenv('CB_PASSPHRASE')
        cb_bot = CoinbaseBot(args.amount, args.token, cb_api_key, cb_secret_key, cb_passphrase)
        result = cb_bot.run()
        if args.chatid:
            telebot = TelegramBot(os.getenv("TELEGRAM_API_KEY"))
            telebot.send_message(result)
        else:
            print(result)
        
    elif args.binance:
        binance_api_key = os.getenv("BINANCE_API_KEY")
        binance_secret_key = os.getenv("BINANCE_SECRET_KEY")
        bot = BinanceBot(args.amount, args.token, binance_api_key, binance_secret_key)
        result = bot.run()
        if args.chatid:
            telebot = TelegramBot(os.getenv("TELEGRAM_API_KEY"))
            telebot.send_message(result)
        else:
            print(result)
    else:
        print("Please add a --coinbase or --binance argument")
    