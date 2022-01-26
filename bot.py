import asyncio
from dotenv import load_dotenv
import argparse
import os
import json
import telebot
from components.utils import daysLeftInMonth, calculateSplitFromDaysLeft
from components.BinanceDCABot import BinanceBot
from components.CoinbaseDCABot import CoinbaseBot
from components.TelegramBot import TelegramBot
from components.CryptocomDCABot import CryptoDotBot



if __name__ =="__main__":
    parser = argparse.ArgumentParser(description='Dollar Cost Averaging Bot that works on Coinbase Pro or Binance, this should be run via CRON')
    parser.add_argument('--coinbase', action="store_true",
                        help='Use the Coinbase DCA', required=False)
    parser.add_argument('--binance', action="store_true",
                        help='Use the Binance DCA', required=False)
    parser.add_argument('--cryptodotcom', action="store_true",
                        help='Use the Crypto.com Exchange DCA', required=False)
    parser.add_argument('--amount', action="store", help="The amount you would like to invest e.g 10.00", required=False)
    parser.add_argument('--tokens', action="store", help="The token you wish to buy e.g ADA-GBP, or a list e.g ADA-GBP, ETH-GBP", required=False)
    parser.add_argument('--findchatid', action="store_true", help="Flag to use to find your chat ID for your bot", required=False)
    parser.add_argument('--chatid', action="store", help="If set, this will cause the bot to send you a message depending on how the trade goes", required=False)
    parser.add_argument('--config', action="store", help="A config file can be used when buying multiple different pairs for different exchanges", required=False)
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
        tokens = args.tokens.split(",")
        if len(tokens) == 1:
            # cb_bot = CoinbaseBot(args.token, cb_api_key, cb_secret_key, cb_passphrase, args.amount, auto=False)
            cb_bot = CoinbaseBot(args.token, args.amount, cb_api_key, cb_secret_key, cb_passphrase)
            result = cb_bot.run()
        if len(tokens) > 1:
            cb_bot = CoinbaseBot(None, None, cb_api_key, cb_secret_key, cb_passphrase)
            total = cb_bot.get_account_holdings_workaround("GBP")[0].get("balance")
            amount_per_token = (calculateSplitFromDaysLeft(daysLeftInMonth(), len(tokens), total))
            if amount_per_token < 5:
                result = f"Insufficient Funds - Would be buying {amount_per_token} of each token"
            else:
                for token in tokens:
                    cb_bot = CoinbaseBot(token, amount_per_token, cb_api_key, cb_secret_key, cb_passphrase)
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

    elif args.cryptodotcom:
        cdc_api_key = os.getenv('CDC_API_KEY')
        cdc_secret_key = os.getenv('CDC_SECRET_KEY')
        bot = CryptoDotBot(cdc_api_key, cdc_secret_key)
        asyncio.run(bot.run(args.token, args.amount))
    
    elif args.config: 
        ## config based approach
        with open(args.config, "r") as config_file:
            config_data = json.load(config_file)
        telegram_id = config_data.get("telegram_chat_id")
        telebot = TelegramBot(os.getenv("TELEGRAM_API_KEY"), telegram_id)
        for pair in config_data.get("pairs"):
            trade_made = False
            if pair.get("exchange").lower() == "binance":
                binance_api_key = os.getenv("BINANCE_API_KEY")
                binance_secret_key = os.getenv("BINANCE_SECRET_KEY")
                bot = BinanceBot(pair.get("amount"), pair.get("pair"), binance_api_key, binance_secret_key)
                result = bot.run()
                #TODO Actually check the results.
                trade_made = True

            elif pair.get("exchange").lower() == "coinbase":
                cb_api_key = os.getenv('CB_API_KEY')
                cb_secret_key = os.getenv('CB_SECRET_KEY')
                cb_passphrase = os.getenv('CB_PASSPHRASE')
                cb_bot = CoinbaseBot(pair.get("pair"), pair.get("amount"), cb_api_key, cb_secret_key, cb_passphrase)
                result = cb_bot.run()
                trade_made = True
            elif pair.get("exchange").lower() == "cryptodotcom":
                cdc_api_key = os.getenv('CDC_API_KEY')
                cdc_secret_key = os.getenv('CDC_SECRET_KEY')
                bot = CryptoDotBot(cdc_api_key, cdc_secret_key)
                result = asyncio.run(bot.run(pair.get("pair"), pair.get("amount")))
                if result:
                    trade_made = True
            else:
                print(f"Exchange {pair.get('exchange')} Not Found...")
            if trade_made:
                telebot.send_message(result)
            print(result)
            

                    

    else:
        print("Please add a --coinbase or --binance argument")
    