from components.BinanceDCABot import BinanceBot
from components.CoinbaseDCABot import CoinbaseBot
from dotenv import load_dotenv
import argparse
import os



if __name__ =="__main__":
    parser = argparse.ArgumentParser(description='Dollar Cost Averaging Bot that works on Coinbase Pro or Binance, this should be run via CRON')
    parser.add_argument('--coinbase', action="store_true",
                        help='Use the coinbase DCA', required=False)
    parser.add_argument('--binance', action="store_true",
                        help='Use the binance DCA', required=False)
    parser.add_argument('--amount', action="store", help="The amount you would like to invest e.g 10.00", required=True)
    parser.add_argument('--token', action="store", help="The token you wish to buy e.g ADA-GBP", required=True)
    load_dotenv()
    args = parser.parse_args()
    #argparse sets unset arguments to None
    if args.coinbase:
        cb_api_key = os.getenv('CB_API_KEY')
        cb_secret_key = os.getenv('CB_SECRET_KEY')
        cb_passphrase = os.getenv('CB_PASSPHRASE')
        cb_bot = CoinbaseBot(args.amount, args.token, cb_api_key, cb_secret_key, cb_passphrase)
        cb_bot.run()
    elif args.binance:
        binance_api_key = os.getenv("BINANCE_API_KEY")
        binance_secret_key = os.getenv("BINANCE_SECRET_KEY")
        bot = BinanceBot(args.amount, args.token, binance_api_key, binance_secret_key)
        bot.run()
    else:
        print("Please add a --coinbase or --binance argument")
    