import http.client
import json
import login as l 
from smartapi.smartConnect import SmartConnect
import pandas as pd


class get_historical:
    def __init__(self, symboltoken, interval, fromdate, todate):
        self.conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
        self.obj = SmartConnect(api_key=l.api_key)
        self.data = self.obj.generateSession( l.user_name, l.password, l.totp)
        self.refreshToken = self.data['data']['refreshToken']
        self.bt = self.data['data']['jwtToken']
        self.payload = {
            "exchange" : "NSE",
            "symboltoken" : symboltoken,
            "interval" : interval,
            "fromdate" : fromdate,
            "todate" : todate
        }
        self.headers = headers = {
            'X-PrivateKey': l.api_key,
            'Accept': 'application/json',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
            'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
            'X-MACAddress': 'MAC_ADDRESS',
            'X-UserType': 'USER',
            'Authorization': self.bt ,
            'Accept': 'application/json',
            'X-SourceID': 'WEB',
            'Content-Type': 'application/json'
        }
    def get_data(self):
        self.conn.request("POST", "/rest/secure/angelbroking/historical/v1/getCandleData", json.dumps(self.payload), self.headers)
        res = self.conn.getresponse()
        data = res.read()
        df_arr = json.loads(data.decode("utf-8"))['data']
        df = pd.DataFrame(df_arr, columns =['Time', 'Open', 'High', 'Low', 'Close', 'Volume']) 
        return df
