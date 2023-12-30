from api_library.api_core import CoinDCXAPICore

class CoinDCXAPIUser(CoinDCXAPICore):
    def get_balances(self):
        url = self.base_url + '/exchange/v1/users/balances'
        return self.make_post_request(url, {})

    def get_balance(self, currency):
        url = self.base_url + '/exchange/v1/users/balances'
        data = self.make_post_request(url, {})
        for balance in data:
            if balance['currency'] == currency:
                return balance

    def get_user_info(self):
        url = self.base_url + '/exchange/v1/users/info'
        return self.make_post_request(url, {})
