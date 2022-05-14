# -*- coding: utf-8 -*-
"""
Created on Fri May  6 19:18:58 2022

@author: shoma
"""

import requests
import json

endPoint = 'https://api.coin.z.com/public'
path     = '/v1/klines?symbol=BTC&interval=1min&date=20210417'

response = requests.get(endPoint + path)
df = json.dumps(response.json(), indent=2)