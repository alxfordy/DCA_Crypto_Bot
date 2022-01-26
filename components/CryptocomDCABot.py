'''
@author: Alex F
'''

import time
import math
import os
import logging
import json
import asyncio

import cryptocom.exchange as cro

class CryptoDotBot():

    def __init__(self, api_key, secret_key):
        """ Initialisation of the Bot with the DCA options """
        self._logger = logging.getLogger("Crypto.com-DCA-Bot")
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        # self.amount = amount
        # self.crypto_token = crypto_token
        self._api_key = api_key
        self._secret_key = secret_key
        self._exchange = cro.Exchange()
        self._account = cro.Account(api_key=self._api_key, api_secret=self._secret_key)
        self._loop = asyncio.new_event_loop()
        self._loop.run_until_complete(self._account.sync_pairs())

    async def _get_account_funds(self, asset=None):
        exchange_balances = await self._account.get_balance()
        #    Returns an array of this Coin(exchange_name='RNDR'): Balance(total=0, available=0, in_orders=0, in_stake=0, coin=Coin(exchange_name='RNDR'))
        non_zero_balances = list()
        if asset:
            for coin in exchange_balances.keys():
                if coin.exchange_name == asset:
                    self._logger.info(f"{exchange_balances[coin].available} of {coin.exchange_name} available")
                    return [exchange_balances[coin]]
                else:
                    continue
            return None
        else:
            for asset_balance in exchange_balances.values():
            #    print(type(asset_balance.available))
            #    print(asset_balance.available)
                if asset_balance.available > 0:
                    self._logger.info(f"{asset_balance.available} of {asset_balance.coin.exchange_name} available")
                    non_zero_balances.append(asset_balance)
        return non_zero_balances

    async def run(self, pair, amount):
        balances, exchange_pairs = await asyncio.gather(self._get_account_funds(), self._exchange.get_pairs())
        buy_asset = pair.split("_")[1]
        available_funds = False
        print(balances)
        for balance in balances:
            if balance.coin.exchange_name == buy_asset:
                if balance.available < int(amount):
                    self._logger.info(f"Insufficient Funds to make {amount} purchase. Current amount {buy_asset} is {balance.available}")
                    available_funds = False
                    return None
                else:
                    available_funds = True
        if available_funds:
            for exchange_pair in exchange_pairs:
                if pair == exchange_pair.exchange_name:
                    self._logger.info(f"Pair {pair} is on Exchange as {exchange_pair}")
                    pair_to_purchase = exchange_pair
            if not exchange_pair:
                return "Pair Not Found..."
            ## Get the price of the pair
            pair_price = await self._exchange.get_price(pair_to_purchase)
            self._logger.info(f"About to Purchase {pair_to_purchase} for {pair_price}")
            return await self._account.buy_market(pair_to_purchase, amount)

if __name__ == "__main__":
    bot = CryptoDotBot("10", "ETH/GBP", "", "")
    asyncio.run(bot._get_account_funds(asset="USDC"))
    asyncio.run(bot.run("ETH_USDC", 3))