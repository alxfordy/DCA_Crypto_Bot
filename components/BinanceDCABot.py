'''
@author: Alex F
'''

import time
import math
import os
import logging
import json
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

class BinanceBot():

    def __init__(self, amount, crypto_token, api_key, secret_key):
        """ Initialisation of the Bot with the DCA options """
        self._logger = logging.getLogger("Binance-DCA-Bot")
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.amount = amount
        self.crypto_token = crypto_token
        self._api_key = api_key
        self._secret_key = secret_key
        self.binance_client = Client(self._api_key, self._secret_key)

    def _get_order_book(self):
        return self.binance_client.get_order_book(self.crypto_token)


    def get_balance(self, asset=None):
        asset = asset if asset else "GBP"
        return self.binance_client.get_asset_balance(asset=asset)

    def get_ticker_price(self, ticker=None):
        """
            This will get the current price for the trading pair that you give the bot at start.
        """
        ticker = ticker if ticker else self.crypto_token
        return self.binance_client.get_symbol_ticker(symbol=ticker)

    @classmethod
    def _floor(cls,step_size):
        return int(round(-math.log(step_size, 10), 0))

    def _get_quantity(self, ticker=None, amount=None, step_size=None):
        ticker = ticker if ticker else self.crypto_token
        amount = amount if amount else self.amount
        step_size = float(step_size) if step_size else float(self._step_size)
        ## Get the ticker price to work out quantity
        ticker_price = self.get_ticker_price(ticker).get("price")
        self._logger.info(f"Calculating Invest Amount {amount} at cost of {ticker_price} step size of {step_size}")
        # times by 0.995 to ensure we don't over order and cause an error
        quantity = float(amount) / float(ticker_price) * 0.995
        return float(round(quantity, BinanceBot._floor(step_size)))

    
    def _get_symbol_info(self, ticker=None):
        ticker = ticker if ticker else self.crypto_token
        return self.binance_client.get_symbol_info(ticker)

    def _got_funds(self):
        if not hasattr(self, 'balance'):
            self.balance = self.get_balance().get("free")
        if self.amount > self.balance:
            return False 
        return True


    def create_buy_order(self, quantity):
        try:
            order = self.binance_client.create_order(
                symbol=self.crypto_token,
                side='BUY',
                type='MARKET',
                quantity=quantity
            )
        except BinanceAPIException as e:
            self._logger.error(f"Binance API Error {e}")
            return False
        except BinanceOrderException as e:
            self._logger.error(f"Binance Order Exception {e}")
            return False
        except Exception as e:
            self._logger.error(f"Issue processing order {e}")
            return False
        return order



    def run(self, **kwargs):
        asset = kwargs.get("asset") if kwargs.get("asset") else "GBP"
        balance = self.get_balance(asset)
        self.balance = balance.get('free')
        self._logger.info(f"You currently have {balance.get('free')} {balance.get('asset')}")
        if not self._got_funds():
            self._logger.error("You haven't got enough funds")
            success = False
            return success
        price = self.get_ticker_price()
        self._logger.info(f"The price of {price.get('symbol')} is {price.get('price')}")
        print(self._get_symbol_info())
        for filter in self._get_symbol_info().get("filters"):
            if filter.get("filterType") == "LOT_SIZE":
                self._step_size = filter.get("stepSize")
        quantity = self._get_quantity()
        self._logger.info(f"About to buy {quantity} of {self.crypto_token}")
        success = self.create_buy_order(quantity)
        self._logger.info(f"Results of the Buy order - {success}")
        return success