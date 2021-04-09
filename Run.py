# To add an interface

# Uncomment following and add appropriate details and run this file
from Client import Client
from Interface import MACDStrat
from Tradeway import processor

print("Enter email registered at 5Paisa: ")
email=input()
print("Enter password ")
password=input()
print("Enter date of birth in yyyymmdd format ")
yyyymmdd_date_of_birth=input()
print("Enter encrypted user id from 5Paisa api portal ")
encrypted_user=input()
print("Enter encrypted password from 5Paisa api portal ")
encrypted_password=input()
print("Enter key from 5Paisa api portal ")
key=input()
client = Client(email, password, yyyymmdd_date_of_birth, encrypted_user, encrypted_password,
                    key)

print("Enter MACD short window length")
short_window=input()
print("Enter MACD long window length")
long_window=input()
print("Enter MACD signal length")
signal=input()
print("Enter length of MACD to view on graph(X-axis)")
series_len=input()
print("Enter scrip code to trade")
scrip_code=input()
#This paramerter is used to generate buy, sell signal
print("Enter Macd threshold (will buy stocks if crossover is below this threshold)")
macd_limit=input()
print("Enter scrip number that user wants to trade, from 5Paisa portal ")
scrip_num=input()
strat = MACDStrat(short_window,long_window,signal,series_len, client,scrip_code,macd_limit ,scrip_num)
print("Enter amount of quantity user wants to trade")
trade_qty=input()

''' this is the actual margin above which the stocks get sold. 
 Whenever macd gives a sell signal, if value of stock is above buyprice+gap only then the stocks are sold 
else user gets dilevery of those stocks. Thereby we make sure that stocks are never sold incurring a loss.'''

print("Enter the margin above which stocks should be sold")
gap=input()
print("Enter the tick time")
tick_time=input()
pl = processor(strat,trade_qty,gap,tick_time)
pl.start_trade()