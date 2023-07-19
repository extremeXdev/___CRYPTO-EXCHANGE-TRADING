from binance.client import Client
import config

class ConnectClient:
    def make_connection(self):
        #Write your api keys here
        api_key = ""
        api_secret = ""
        
        return Client(api_key, api_secret)