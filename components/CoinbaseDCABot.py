'''
@author: Alex F
'''

import logging
import cbpro

class CoinbaseBot():

    def __init__(self, crypto_token, amount, api_key, secret_key, passphrase):
        """ Initialisation of the Bot with the DCA options """
        self._logger = logging.getLogger("Coinbase-DCA-Bot")
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.amount = amount
        self.crypto_token = crypto_token
        self._api_key = api_key
        self._secret_key = secret_key
        self._passphrase = passphrase
        self.coinbase_client = cbpro.AuthenticatedClient(self._api_key, self._secret_key, self._passphrase)
        self.profile_id = self.get_accounts()[0].get("profile_id")

    def get_accounts(self):
        return(self.coinbase_client.get_accounts())

    def get_account_holdings(self):
        ## THIS GENERATOR IS DOG SHIT 
        print(self.profile_id)
        results = self.coinbase_client.get_account_holds(self.profile_id)
        for key, value in results:
            print(f"{key}: {value}")
        print(type(results))
        print(results[0].get("message"))
    
    def get_account_holdings_workaround(self, ticker=None):
        if ticker:
            return [item for item in self.get_accounts() if item.get("currency") == ticker]
        else: return self.get_accounts()
    
    def get_ticker_price(self, ticker=None):
        ticker = ticker if ticker else self.crypto_token
        return self.coinbase_client.get_product_ticker(product_id=ticker)

    def _got_funds(self, asset=None):
        asset = asset if asset else "GBP"
        if not hasattr(self, 'balance'):
            self.balance = self.get_account_holdings_workaround(asset)[0].get("balance")
        if float(self.amount) > float(self.balance): return False 
        return True

    def create_buy_order(self):
        result = self.coinbase_client.place_market_order(product_id=self.crypto_token, 
                               side='buy', 
                               funds=self.amount)
        if "message" in result:
        # Something went wrong if there's a 'message' field in response
            print(result['message'])
        return result

    def run(self, **kwargs):
        asset = kwargs.get("asset") if kwargs.get("asset") else "GBP"
        balance = self.get_account_holdings_workaround(asset)
        if len(balance) > 1:
            self._logger(f"Issues with checking FIAT Balance - More than one returned")
            return f"Issues with checking FIAT Balance - More than one returned"
        fiat_balance = balance[0]
        self.balance = fiat_balance.get('balance')
        self._logger.info(f"You currently have {fiat_balance.get('available')} {fiat_balance.get('currency')}")
        if not self._got_funds():
            self._logger.error("You haven't got enough funds")
            return f"Error - Not Enough Funds - Balance: {fiat_balance.get('available')} {fiat_balance.get('currency')} and want to buy {self.amount} {fiat_balance.get('currency')}"
        
        ticker_price_details = self.get_ticker_price()
        self._logger.info(f"Buying {self.amount} of {self.crypto_token} at {ticker_price_details.get('price')}")
        result = self.create_buy_order()
        ## result looks like 
        # return {'id': '6ea1e040-d8b5-4cb0-9f6e-94585dc13960', 'product_id': 'SOL-GBP', 'side': 'buy', 'stp': 'dc', 'funds': '9.950248', 'specified_funds': '10.00', 'type': 'market', 'post_only': False, 'created_at': '2021-08-03T17:36:26.13214Z', 'fill_fees': '0', 'filled_size': '0', 'executed_value': '0', 'status': 'pending', 'settled': False}
        return "Success"