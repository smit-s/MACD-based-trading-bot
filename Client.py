from py5paisa import FivePaisaClient
from py5paisa.order import Order, OrderType, Exchange, OrderFor, RequestList, AHPlaced, ExchangeSegment
import time
import http
import requests
import json
from auth import EncryptionClient
import logging
from logging import handlers

BODY = "body"

APP_VER = "1.0"
LOGIN_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/LoginRequestMobileNewbyEmail"
HEADERS = {'Content-Type': 'application/json'}
APP_NAME = "5P56105291"


class Client:
    # encrypted_usr, encrypted_pass, key are redundant and should be removed
    def __init__(self, email, pswd, dob, encrypted_usr, encrypted_pass, key):
        """

        :param email:
        :param pswd:
        :param dob:
        :param encrypted_usr: from 5paisa
        :param encrypted_pass: from 5paisa
        :param key: from 5paisa
        """
        self.email = email
        self.pswd = pswd
        self.dob = dob
        self.key = key
        self.encrypted_usr = encrypted_usr
        self.encrypted_pass = encrypted_pass
        # Here  dob=yyyymmdd
        self.session = requests.Session()
        self.payload = {
            "head": {"appName": APP_NAME, "appVer": APP_VER, "key": self.key, "osName": "WEB", "requestCode": "",
                "userId": self.encrypted_usr, "password": self.encrypted_pass}, "body": {"ClientCode": ""}}

        self.logger = logging.getLogger('Client')
        logHandler = handlers.RotatingFileHandler('Client.log', maxBytes=500, backupCount=20 )
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logHandler)

    def login(self):
        encryption_client = EncryptionClient()
        secret_email = encryption_client.encrypt(self.email)
        secret_passwd = encryption_client.encrypt(self.pswd)
        secret_dob = encryption_client.encrypt(self.dob)
        self.payload[BODY]["Email_id"] = secret_email
        self.payload[BODY]["Password"] = secret_passwd
        self.payload[BODY]["My2PIN"] = secret_dob
        self.payload["head"]["requestCode"] = "5PLoginV2"
        res = self._login_request(LOGIN_ROUTE)
        # self.cookies = res.cookies.get_dict()
        # print(self.cookies)
        res = res.json()
        message = res[BODY]["Message"]
        if message == "":
            self.logger.debug("Logged in!!")
            print("Logged in!!")
        else:
            self.logger.debug(message)
            print(message)
        self.client_code = str(res[BODY]["ClientCode"])

    def _login_request(self, route):
        return self.session.post(route, json=self.payload, headers=HEADERS)

    def place_order(self, order_type,  qty,scrip_code, price,ahPlaced):
        """
        There are many variables in request that are hardcoded and can be made vriable as per users requirement.

        :param order_type: 'b' for buy and 's' for sell
        :param qty: quantity of shares to trade
        :param scrip_code: scrip code from 5paisa for example 1023 for federalbank
        :param price: price at which trade required to be executed.
        :param ahPlaced: placed after hours or in normal markert.
        :return:
        """
        self.login()
        try:
            if 'b' == str.lower(order_type):
                order = "BUY"
            elif ('s' == str.lower(order_type)):
                order ="SELL"
            else:
                print('Wrong order type')

            url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/OrderRequest"
            payload = {"head": {"appName": APP_NAME, "appVer": APP_VER, "key": self.key, "osName": "WEB",
                "requestCode": "5POrdReq", "userId": self.encrypted_usr, "password": self.encrypted_pass},
                "body": {"ClientCode": str(self.client_code), "OrderFor": "P", "Exchange": "N", "ExchangeType": "C",
                    "Price": price, "OrderID": 0, "OrderType": order, "Qty": qty, "OrderDateTime": "/Date(1610611860)/",
                    "ScripCode": scrip_code, "AtMarket": False, "RemoteOrderID": 1, "ExchOrderID": 0,
                    "DisQty": 0, "IsStopLossOrder": False, "StopLossPrice": 0, "IsVTD": False, "IOCOrder": False,
                    "IsIntraday": False, "PublicIP": "192.168.1.1", "AHPlaced": ahPlaced,
                    "ValidTillDate": "/Date(1611598260)/", "iOrderValidity": 0, "TradedQty": 0,
                    "OrderRequesterCode": str(self.client_code), "AppSource": "4532"}}
            response = self.session.request("POST", url, headers=HEADERS, data=json.dumps(payload))
            self.logger.debug(response.text)
            print(response.text)
            return json.loads(response.text)
        except TypeError as err:
            self.logger.error(err)
            print(err)

    def get_orders(self):
        """
        Fetch all orders of that specific day. Inlcudes canceled orders as well
        :return:
        """
        self.login()
        url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/OrderBook"
        payload = {"head": {"appName": APP_NAME, "appVer": APP_VER, "key": self.key, "osName": "WEB",
            "requestCode": "5POrdBkV2", "userId": self.encrypted_usr, "password": self.encrypted_pass},
            "body": {"ClientCode": str(self.client_code)}}
        response = self.session.request("POST", url, headers=HEADERS, data=json.dumps(payload))
        self.logger.debug(response.text)
        print(response.text)
        data = json.loads(response.text)
        return data["body"]["OrderBookDetail"]

    def get_positions(self):
        """
        Get list of open positions.
        :return:
        """
        self.login()
        url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/NetPositionNetWise"
        payload = {"head": {"appName": APP_NAME, "appVer": APP_VER, "key": self.key, "osName": "WEB",
            "requestCode": "5PNPNWV1", "userId": self.encrypted_usr, "password": self.encrypted_pass},
            "body": {"ClientCode": str(self.client_code)}}
        response = self.session.request("POST", url, headers=HEADERS, data=json.dumps(payload))
        self.logger.debug(response.text)
        print(response.text)
        data = json.loads(response.text)
        return data["body"]["NetPositionDetail"]

    #function not used anywhere.
    def get_holdings(self):
        """
        Get list of current holdings
        :return:
        """
        self.login()
        url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/Holding"
        payload = {"head": {"appName": APP_NAME, "appVer": APP_VER, "key": self.key, "osName": "WEB",
            "requestCode": "5PHoldingV2", "userId": self.encrypted_usr, "password": self.encrypted_pass},
            "body": {"ClientCode": str(self.client_code)}}
        response = self.session.request("POST", url, headers=HEADERS, data=json.dumps(payload))
        self.logger.info(response.text)
        print(response.text)
        data = json.loads(response.text)
        return data["body"]["Data"]

    def modify_orders(self, order_id, qty, scrip_code, price,ahPlaced):
        """

        :param order_id: id of order to be modified.
        :param qty: new quantity
        :param scrip_code: scrip code from 5paisa for example 1023 for federalbank
        :param price: price at which trade required to be executed.
        :param ahPlaced: placed after hours or in normal markert.
        :return:
        """
        self.login()
        url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/OrderRequest"
        payload = {"head": {"appName": APP_NAME, "appVer": APP_VER, "key": self.key, "osName": "WEB",
        "requestCode": "5POrdReq", "userId": self.encrypted_usr, "password": self.encrypted_pass},
         "body": {"ClientCode": str(self.client_code), "OrderFor": "M", "Exchange": "N", "ExchangeType": "C",
                 "Price": price, "OrderID": 0, "OrderType": "BUY", "Qty": qty, "OrderDateTime": "/Date(1610611860)/",
                 "ScripCode": scrip_code, "AtMarket": False, "RemoteOrderID": 1, "ExchOrderID": order_id, "DisQty": 0,
                 "IsStopLossOrder": False, "StopLossPrice": 0, "IsVTD": False, "IOCOrder": False,
                 "IsIntraday": False, "PublicIP": "192.168.1.1", "AHPlaced": ahPlaced,
                 "ValidTillDate": "/Date(1611598260)/", "iOrderValidity": 0, "TradedQty": 0,
                    "OrderRequesterCode": str(self.client_code), "AppSource": "4532"}}
        response = self.session.request("POST", url, headers=HEADERS, data=json.dumps(payload))
        self.logger.debug(response.text)
        print(response.text)
        data = json.loads(response.text)
        return data

    def cancel_order(self, order_id, qty, scrip_code,ahPlaced):
        """

        :param order_id: id of order to be modified.
        :param qty: new quantity
        :param scrip_code: scrip code from 5paisa for example 1023 for federalbank
        :param ahPlaced: placed after hours or in normal markert.
        :return:
        """
        self.login()
        url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/OrderRequest"
        payload = {"head": {"appName": APP_NAME, "appVer": APP_VER, "key": self.key, "osName": "WEB",
        "requestCode": "5POrdReq", "userId": self.encrypted_usr, "password": self.encrypted_pass},
         "body": {"ClientCode": str(self.client_code), "OrderFor": "C", "Exchange": "N", "ExchangeType": "C",
                 "Price": 0, "OrderID": 0, "OrderType": "BUY", "Qty": qty, "OrderDateTime": "/Date(1610611860)/",
                 "ScripCode": scrip_code, "AtMarket": False, "RemoteOrderID": 1, "ExchOrderID": order_id, "DisQty": 0,
                 "IsStopLossOrder": False, "StopLossPrice": 0, "IsVTD": False, "IOCOrder": False,
                 "IsIntraday": False, "PublicIP": "192.168.1.1", "AHPlaced": ahPlaced,
                 "ValidTillDate": "/Date(1611598260)/", "iOrderValidity": 0, "TradedQty": 0,
                    "OrderRequesterCode": str(self.client_code), "AppSource": "4532"}}
        response = self.session.request("POST", url, headers=HEADERS, data=json.dumps(payload))
        self.logger.debug(response.text)
        print(response.text)
        data = json.loads(response.text)
        return data

    def get_tick(self, scrip_code):
        """

        :param scrip_code: scrip code from 5paisa for example 1023 for federalbank
        :return:
        """
        try:
            self.login()
            url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/MarketFeed"
            payload = {"head": {"appName": APP_NAME, "appVer": APP_VER, "key": self.key, "osName": "Android",
                "requestCode": "5PMF", "userId": self.encrypted_usr, "password": self.encrypted_pass},
                "body": {"Count": 10, "MarketFeedData": [
                    {"Exch": "N", "ExchType": "C", "Symbol": str(scrip_code), "Expiry": "", "StrikePrice": "0",
                        "OptionType": ""}], "ClientLoginType": 0, "LastRequestTime": "/Date(0)/", "RefreshRate": "H"}}
            response = self.session.request("POST", url, headers=HEADERS, data=json.dumps(payload))
            print(response.text)
            data = json.loads(response.text)
            frame = {'scrip_code': scrip_code, 'price': data['body']['Data'][0]['LastRate'],
                'time': data['body']['Data'][0]['TickDt']}
            self.logger.debug(data)
            return frame
        except:
            print("Error while fetching tick data")
            self.logger.debug("Error while fetching tick data")

# Create a processor. Add following details
#
# client = Client(email, password, yyyymmdd date of birth, encrypted user, encrypted password,
#                     key)


# Example
# print(client.get_tick("FEDERALBNK"))
# print(client.cancel_order("383893445", 5, 1023,"Y"))



