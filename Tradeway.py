import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Interface import MACDStrat
from Client import Client
import pandas as pd
import time
import logging
from logging import handlers
import datetime

class processor:
    def __init__(self,strat, trade_qty, gap):
        """

        :param trade_qty: quantity of shares to trade.
        :param gap: difference between sell and buy price at which a sell is triggered.
        """
        self.strat = strat
        self.gap = gap
        self.qty = trade_qty
        plt.ion()
        self.fig, self.ax = plt.subplots(2)
        self.prices, self.ydata1 = [i for i in range(len(self.strat.prices.to_list()))], self.strat.prices.to_list()
        self.ema, self.ydata2 = [i for i in range(len(self.strat.ema.to_list()))], self.strat.ema.to_list()
        self.macd, self.ydata3 = [i for i in range(len(self.strat.macd.to_list()))], self.strat.macd.to_list()
        self.xdata4, self.ydata4 = [], []
        self.ln, = self.ax[0].plot([], [], lw=1)
        self.ln2, = self.ax[1].plot([], [], lw=1, label="ema")
        self.ln3, = self.ax[1].plot([], [], lw=1, label='macd')
        self.ln4, = self.ax[1].plot([], [], 'ro', label='cross')
        self.logger = logging.getLogger('Tradeway')
        logHandler = handlers.RotatingFileHandler('tradeway.log', maxBytes=2000000, backupCount=20)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logHandler)

    def position_exist(self,arr):
        for i in range(len(arr)):
            if(arr[i]["ScripName"]==self.strat.scrip_code and float(arr[i]["BuyAvgRate"])>0):
                return True
        return False

    def execute_trade(self, sig, price):
        """

        :param sig: buy or sell or hold
        :param price: price at which order shall be placed.
        """
        self.logger.debug("Date- "+str(datetime.datetime.timestamp()) )
        if (sig == 'buy'):
            #get all poitions
            pos_list = self.strat.client.get_positions()
            self.logger.debug("pos_list- " + str(pos_list))
            #create a new order only if there is no open position to avoid overbuying.
            if (not self.position_exist(pos_list)):
                order_list = self.strat.client.get_orders()
                self.logger.debug("order- " + str(order_list))
                my_order_info = None
                #Check if there are any active buy orders to avoid placing multiple buys.
                for order in order_list:
                    if (order["BuySell"] == 'B' and (order["RequestType"] == 'P' or order["RequestType"] == 'M') and
                            order["ScripCode"] == self.strat.scrip_num and str(
                                    order["OrderStatus"]).lower().__contains__("placed")):
                        my_order_info = order
                        self.logger.debug("my-order- " + str(my_order_info))
                        break
                #If there are no active buy orders place a new one else, modify the existing one.
                if (my_order_info == None):
                    self.logger.debug("placeing new order")
                    self.strat.client.place_order('b', self.qty, self.strat.scrip_num, price, "N")
                else:
                    self.logger.debug("modifying order")
                    exchange_id = str(my_order_info["ExchOrderID"])
                    self.strat.client.modify_orders(exchange_id, int(my_order_info["PendingQty"]), self.strat.scrip_num,
                                                    price, "N")



        elif (sig == 'sell'):
            holding_list=self.strat.client.get_holdings()
            pos_list = self.strat.client.get_positions()
            self.logger.debug("pos_list- " + str(pos_list))
            #create a new sell order only if there is an open position
            if (len(pos_list) > 0):
                my_pos = None
                order_list = self.strat.client.get_orders()
                self.logger.debug("order- " + str(order_list))
                for i in range(len(pos_list)):
                    if (pos_list[i]["ScripName"] == self.strat.scrip_code and float(pos_list[i]["SellAvgRate"]) > 0):
                        my_pos=pos_list[i]
                        break
                my_order_info = None
                for order in order_list:
                    if (order["BuySell"] == 'S' and (order["RequestType"] == 'P' or order["RequestType"] == 'M') and
                            order["ScripCode"] == self.strat.scrip_num and str(
                                order["OrderStatus"]).lower().__contains__("placed")):
                        self.logger.debug("my-order- " + str(my_order_info))
                        my_order_info = order
                        break
                #Sell on basis of price
                self.logger.debug("Buy average- " + str(float(my_pos["BuyAvgRate"])))
                self.logger.debug("sell price proposed- " +  str(price + self.gap))
                if (my_pos!=None and my_order_info == None and float(my_pos["BuyAvgRate"]) > price + self.gap):
                    self.strat.client.place_order('s', self.qty, self.strat.scrip_num, price, "N")
                elif (my_pos!=None and my_order_info != None and float(my_pos["BuyAvgRate"]) > price + self.gap):
                    exchange_id = str(my_order_info["ExchOrderID"])
                    self.strat.client.modify_orders(exchange_id, int(my_order_info["PendingQty"]), self.strat.scrip_num,price, "N")
            # if (len(holding_list) > 0):
            #     my_pos = None
            #     order_list = self.strat.client.get_orders()
            #     self.logger.debug("order- " + str(order_list))
            #     for i in range(len(holding_list)):
            #         if (holding_list[i]["ScripName"] == self.strat.scrip_code and float(holding_list[i]["SellAvgRate"]) > 0):
            #             my_pos = holding_list[i]
            #             break
            #     my_order_info = None
            #     for order in order_list:
            #         if (order["BuySell"] == 'S' and (order["RequestType"] == 'P' or order["RequestType"] == 'M') and
            #                 order["ScripCode"] == self.strat.scrip_num and str(
            #                     order["OrderStatus"]).lower().__contains__("placed")):
            #             self.logger.debug("my-order- " + str(my_order_info))
            #             my_order_info = order
            #             break
            #     # Sell on basis of price
            #     self.logger.debug("Buy average- " + str(float(my_pos["BuyAvgRate"])))
            #     self.logger.debug("sell price proposed- " + str(price + self.gap))
            #     if (my_pos != None and my_order_info == None and float(my_pos["BuyAvgRate"]) > price + self.gap):
            #         self.strat.client.place_order('s', self.qty, self.strat.scrip_num, price, "N")
            #     elif (my_pos != None and my_order_info != None and float(my_pos["BuyAvgRate"]) > price + self.gap):
            #         exchange_id = str(my_order_info["ExchOrderID"])
            #         self.strat.client.modify_orders(exchange_id, int(my_order_info["PendingQty"]), self.strat.scrip_num,
            #                                         price, "N")
            #



    def start_trade(self):
        plt.legend(loc='best')
        while True:
            try:
                time.sleep(40)
                self.logger.debug("=======Start=======")
                # fetch signal and and price
                sig, price, ema, macd = self.strat.update_macd()
                self.logger.debug("signal-" + sig + " price-" + str(price) + " ema-" + str(ema) + " macd-" + str(macd))
                self.execute_trade(sig, price)
                print("signal-", sig, " price-", price, " ema-", ema, " macd-", macd)
                self.ydata1.append(price)
                self.ydata2.append(ema)
                self.ydata3.append(macd)
                if (len(self.ydata1) > self.strat.series_len):
                    del self.ydata1[0:len(self.ydata1) - self.strat.series_len]
                    del self.ydata2[0:len(self.ydata2) - self.strat.series_len]
                    del self.ydata3[0:len(self.ydata3) - self.strat.series_len]

                self.prices = [i for i in range(min(len(self.ydata1), self.strat.series_len))]
                self.ema = [i for i in range(min(len(self.ydata2), self.strat.series_len))]
                self.macd = [i for i in range(min(len(self.ydata3), self.strat.series_len))]
                # if(sig=='buy'or sig=='sell'):
                #     self.ydata4.append(macd)
                #     self.xdata4.append(len(self.xdata1))
                #     temp=[]
                #     temp2=[]
                #     for i in range(len(self.xdata4)):
                #         if(self)
                # self.ln4.set_data(self.xdata4[i if i>len(self.xdata1)-self.strat.series_len for i in self.ydata4],self.ydata4[len(self.ydata4)-self.strat.series_len if len(self.ydata4)>self.strat.series_len else 0:len(self.ydata4)])
                # # self.ax[0].plot(self.xdata1,self.ydata1)
                # self.ax[1].plot(self.xdata1,self.ydata1)

                # update plot
                self.ln.set_data(self.prices, self.ydata1)
                self.ln2.set_data(self.ema, self.ydata2)
                self.ln3.set_data(self.macd, self.ydata3)
                self.ax[0].relim()
                self.ax[0].autoscale_view()
                self.ax[1].relim()
                self.ax[1].autoscale_view()
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
            except Exception as err:
                print(err)


# Uncomment following and add appropriate details and run this file
#
# client = Client(email, password, yyyymmdd date of birth, encrypted user, encrypted password,
#                     key)
# strat = MACDStrat(short_window,long_window,signal,series_len- length of xaxis in graph, client,scrip_code- like "SBIN",macd_limit- the upper and lower bound of macd- will buy below -macd_limit and sell above macd_limit ,scrip_num-scrip code as per 5paisa)
# pl = processor(strat,trade_qty- amount of shares to trade,gap- minimum gap in buy and sell price at above which the shares are actually solc)
# pl.start_trade()