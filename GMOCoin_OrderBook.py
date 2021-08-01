# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 19:52:09 2021

@author: shoma
"""


import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter
import datetime

'''BTC ETH BCH LTC XRP BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY'''
symbol = 'BTC_JPY'


def orderbooks(symbol):
    endPoint = 'https://api.coin.z.com/public'
    path = '/v1/orderbooks?symbol='+symbol

    response = requests.get(endPoint + path)
    data = response.json()['data']

    data_ask = pd.DataFrame(data['asks'])
    data_ask = data_ask.astype({'price': float, 'size': float})
    data_ask.price = round(data_ask.price, -3)
    data_ask = data_ask.groupby('price').sum()
    data_ask = data_ask.reset_index(drop=False)
    data_ask['accm'] = data_ask['size'].cumsum()

    data_bid = pd.DataFrame(data['bids'])
    data_bid = data_bid.astype({'price': float, 'size': float})
    data_bid.price = round(data_bid.price, -3)
    data_bid = data_bid.groupby('price').sum()
    data_bid = data_bid.reset_index(drop=False)
    data_bid = data_bid.sort_values('price', ascending=False)
    data_bid['accm'] = data_bid['size'].cumsum()
    return data_ask, data_bid


def status():
    endPoint = 'https://api.coin.z.com/public'
    path = '/v1/status'
    response = requests.get(endPoint + path)
    data = response.json()['data']['status']
    return data


def ticker(symbol):
    endPoint = 'https://api.coin.z.com/public'
    path = '/v1/ticker?symbol='+symbol
    response = requests.get(endPoint + path)
    data = pd.DataFrame(response.json()['data'])
    data = data.astype({'ask': float,'bid': float,'high': float,'last': float,'low': float,'volume': float})
    return data

'''loop'''
tm = []
allinfo = []
leg = 200

plt.rcParams['font.size'] = 7
plt.rcParams['font.family'] = 'Tahoma'

fig = plt.figure(figsize=(10, 6), facecolor='w',tight_layout=True)
fig.canvas.set_window_title('Order Book')
fig.patch.set_facecolor('lightgray')

axs = [
    fig.add_subplot(2,2,1),
    fig.add_subplot(2,2,2),
    fig.add_subplot(2,2,3),
    fig.add_subplot(2,2,4),
    # fig.add_subplot(5,5,5),
    # fig.add_subplot(5,5,6),

]

def animate(i):
    for ax in axs:
        ax.cla() # ax をクリア
        ax.grid()
        ax.set_facecolor('lightgray')
        ax.xaxis.set_tick_params(rotation=45)
        # ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        ax.title.set_size(11)
        ax.xaxis.label.set_size(7)
        ax.yaxis.label.set_size(7)

    d = ticker(symbol)
    d['sp'] = d['ask'] - d['bid']

    data_bid = orderbooks(symbol)[0]
    data_ask = orderbooks(symbol)[1]

    if len(allinfo) == leg:
        allinfo.pop(0)
    else:
        allinfo.append(d.iloc[0])


    if len(tm) == leg:
        tm.pop(0)
    else:
        tm.append(datetime.datetime.now())

    df_allinfo = pd.DataFrame(allinfo)

    axs[0].plot(tm, df_allinfo['ask'], label = 'ask', color='red')
    axs[0].plot(tm, df_allinfo['last'], label = 'last', color='black')
    axs[0].plot(tm, df_allinfo['bid'], label = 'bid', color='green')
    axs[0].set_title('Rate', size=12, color='black', fontsize=8)
    axs[0].yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,}'))
    # axs[0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    axs[0].legend(loc='upper left')


    axs[1].plot(tm, df_allinfo['sp'], label = 'sp', color='black')
    axs[1].set_title('Spread', size=12, color='black', fontsize=8)
    axs[1].yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,}'))
    # axs[1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    axs[1].legend(loc='upper left')

    lastprice_from = round(round(d['last'][0],-3) + round(d['last'][0],-3) *0.03, -3)
    lastprice_to = round(round(d['last'][0],-3) - round(d['last'][0],-3) *0.03, -3)

    axs[2].scatter(data_ask[data_ask['price'] >= lastprice_to]['price'],data_ask[data_ask['price'] >= lastprice_to]['size'], s= 5, marker='x', color='darkred')
    axs[2].scatter(data_bid[data_bid['price'] <= lastprice_from]['price'],data_bid[data_bid['price'] <= lastprice_from]['size'], s= 5, marker='x', color='darkblue')
    axs[2].xaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,}'))
    axs[2].set_xlim([round(lastprice_from, -4), round(lastprice_to, -4)])
    axs[2].set_ylim([0, 30])

    axs[3].scatter(data_ask['price'],data_ask['size'], s= 5, marker='x', color='darkred')
    axs[3].scatter(data_bid['price'],data_bid['size'], s= 5, marker='x', color='darkblue')
    axs[3].plot(data_ask['price'],data_ask['accm'], color='red')
    axs[3].plot(data_bid['price'],data_bid['accm'], color='blue')
    axs[3].xaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,}'))
    axs[3].set_xlim([2500000, 4500000])
    axs[3].set_ylim([0, 150])

ani = FuncAnimation(fig, animate, interval = 2000)

plt.tight_layout()
plt.show()


