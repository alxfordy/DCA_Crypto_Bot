# DCA Bot For All

This is a bot that will create buy orders on Binance and Coinbase Pro with your available funds. It doesn't pull money from your bank account yet.

Usage
```
usage: bot.py [-h] [--coinbase] [--binance] --amount AMOUNT --token TOKEN

Dollar Cost Averaging Bot that works on Coinbase Pro or Binance, this should be run via CRON

optional arguments:
  -h, --help       show this help message and exit
  --coinbase       Use the coinbase DCA
  --binance        Use the binance DCA
  --amount AMOUNT  The amount you would like to invest e.g 10.00
  --token TOKEN    The token you wish to buy e.g ADA-GBP
```

I've set this up in AWS Lambda and it runs once every 5 days, you can do the same with CRON on a server. Just generate API keys for either Binance or CoinbasePro, put them in your .env file and away you go.

How to set it up on AWS Lamnda - https://alexford9296.medium.com/dollar-cost-averaging-bot-for-binance-and-coinbase-pro-6b9be7ca074b

To Do -
- [ ] Discord message when buy order created to see if it as successful or failed.
- [ ] (optional) - Pull money from bank account

