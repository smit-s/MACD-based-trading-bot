from pymongo import MongoClient
import pandas as pd


class MACDStrat:

    def proc(self):
        #fetch data from database for calculation of macd
        time_series=[doc for doc in self.data.find({"scrip_code":self.scrip_code})]
        time_series.sort(key=lambda doc:doc["time"])
        self.prices=pd.Series([doc.get('price') for doc in time_series])
        if(len(self.prices)>self.series_len):
            self.prices=self.prices[-1-self.series_len:len(self.prices)-1]
        self.ema_short=self.prices.ewm(span=self.short_window).mean()
        self.ema_long=self.prices.ewm(span=self.long_window).mean()
        self.macd=self.ema_short-self.ema_long
        self.ema=self.macd.ewm(span=self.signal).mean()


    def __init__(self,short_window,long_window,signal,series_len, client,scrip_code,macd_limit,scrip_num):
        self.short_window=short_window
        self.long_window=long_window
        self.signal=signal
        self.series_len=series_len
        self.client=client
        self.scrip_num=scrip_num
        self.mongoclient=MongoClient('localhost',27017)
        #database  name
        self.db=self.mongoclient.series_data
        #database collection name
        self.data=self.db.data
        self.scrip_code=scrip_code
        self.macd=pd.Series()
        self.ema=pd.Series()
        self.macd_limit=macd_limit
        self.prices=pd.Series()
        self.proc()

    def update_macd(self):
        """
        Updates macd and return signal, price macd and ema
        :return:
        """
        doc=self.client.get_tick(self.scrip_code)
        if(doc!=None):
            self.data.insert_one(doc)
            self.prices=self.prices.append(pd.Series(doc.get("price")))
            if(self.prices.size>self.series_len):
                self.prices=pd.Series(self.prices.to_list().pop(0))
            #Calculate macd
            if(self.ema_short.size>0 and self.ema_long.size>0):
                new_short=(2/(1+self.short_window))*self.prices.to_list()[self.prices.size-1]+(1-(2/(1+self.short_window)))*self.ema_short.to_list()[self.ema_short.size-1]
                new_long=(2/(1+self.long_window))*self.prices.to_list()[self.prices.size-1]+(1-(2/(1+self.long_window)))*self.ema_long.to_list()[self.ema_long.size-1]
                new_macd=new_short-new_long
            else:
                new_macd=0
                new_short=self.prices.to_list()[self.prices.size-1]
                new_long=self.prices.to_list()[self.prices.size-1]
            self.ema_short=self.ema_short.append(pd.Series(new_short))
            self.ema_long=self.ema_long.append(pd.Series(new_long))
            self.macd=self.macd.append(pd.Series(new_macd))
            #Calculate ema of macd.
            if(self.ema.size>0):
                new_ema=(2/(1+self.signal))*new_macd+(1-(2/(1+self.signal)))*self.ema.to_list()[self.ema.size-1]
            else:
                new_ema=new_macd
            self.ema=self.ema.append(pd.Series(new_ema))
            #Decide signal on basis of macd.
            if(self.macd.size>3 and self.ema.size>3):
                if(self.macd.to_list()[self.macd.size-2]>self.ema.to_list()[self.ema.size-2] and self.macd.to_list()[self.macd.size-1]<self.ema.to_list()[self.ema.size-1] and self.ema.to_list()[self.ema.size-1]>self.macd_limit):
                    return "sell",doc.get("price"),new_ema,new_macd
                elif(self.macd.to_list()[self.macd.size-2]<self.ema.to_list()[self.ema.size-2] and self.macd.to_list()[self.macd.size-1]>self.ema.to_list()[self.ema.size-1] and self.ema.to_list()[self.ema.size-1]<-self.macd_limit):
                    return "buy",doc.get("price"),new_ema,new_macd
            return "hold",doc.get("price"),new_ema,new_macd






