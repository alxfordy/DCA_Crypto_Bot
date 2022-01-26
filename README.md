# DCA Bot For All

This is a bot that will create buy orders on Binance and Coinbase Pro with your available funds. It doesn't pull money from your bank account yet.

Usage
```
usage: bot.py [-h] [--coinbase] [--binance] [--cryptodotcom] [--amount AMOUNT] [--tokens TOKENS] [--findchatid] [--chatid CHATID] [--config CONFIG]

Dollar Cost Averaging Bot that works on Coinbase Pro or Binance, this should be run via CRON

optional arguments:
  -h, --help       show this help message and exit
  --coinbase       Use the Coinbase DCA
  --binance        Use the Binance DCA
  --cryptodotcom   Use the Crypto.com Exchange DCA
  --amount AMOUNT  The amount you would like to invest e.g 10.00
  --tokens TOKENS  The token you wish to buy e.g ADA-GBP, or a list e.g ADA-GBP, ETH-GBP
  --findchatid     Flag to use to find your chat ID for your bot
  --chatid CHATID  If set, this will cause the bot to send you a message depending on how the trade goes
  --config CONFIG  A config file can be used when buying multiple different pairs for different exchanges
```

I've set this up in AWS Lambda and it runs once every 5 days, you can do the same with CRON on a server. Just generate API keys for either Binance or CoinbasePro, put them in your .env file and away you go.

How to set it up on AWS Lamnda - https://alexford9296.medium.com/dollar-cost-averaging-bot-for-binance-and-coinbase-pro-6b9be7ca074b

There is now support for a config file which will handle multiple pairs with multiple different exchanges.
```
python3 bot.py --config config.json
```
An example config file is provided but something like below works
```json
{
    "pairs": [
        {
            "pair": "ETH_USD",
            "exchange": "cryptodotcom",
            "amount": 10
        },
        {
            "pair": "ALGO-GBP",
            "exchange": "coinbase",
            "amount": 10
        },
        {
            "pair": "BNBBTC",
            "exchange": "binance",
            "amount": 10
        }
    ],
    "telegram_chat_id": 1921878784
}
```

## Telegram

The telegram is very hacky for now but if you run "python3 bot.py --chatid" and send "/start" to your bot username on telegram it will reply with a numeric chat ID.
This Chat-ID is then used to send you messages with how the trade has gone. so you need to run the program like this
```
python3 bot.py --coinbase --amount 10.00 --token "ADA-GBP" --chatid 1921878784
```


To Do -
- [X] Send message on telegram of the result of a trade
- [ ] Telegram functionality needs sorting - productionise start, stop etc
- [ ] Sort out persistent chat ID in telegram


