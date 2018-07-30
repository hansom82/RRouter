# -*- coding: utf-8 -*-
#
# Copyright (c) 2018-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# For more information see the README file.


import requests
from time import sleep


class UsrInfo(object):
    """ Collecting and showing different useful information. """
    
    def __init__(self, display=None, leds=None):
        self.display = display
        self.leds = leds
    
        self.line_height = 11
        self.font_size = 10
        
    def get_cryptocurrencies_rates(self):
        """ Get rates from 'coinmarketcap.com'. """
        api_url = 'https://api.coinmarketcap.com/v1/ticker/?limit=10'
        try:
            data = requests.get(api_url).json()
        except:
            return []
        rates = []
        for currency in data:
            if currency['symbol'] in ['BTC', 'ETH']:
                rates.append({
                    'name': currency['symbol'],
                    'price_usd': currency['price_usd'],
                    'percent_change_24h': currency['percent_change_24h'],
                    'percent_change_7d': currency['percent_change_7d']
                    })
        return rates
    
    def get_usd_eur_rate(self):
        """ Get USD->UAH rate. """
        result = {'USD': 0, 'EUR': 0}
        api_url_tpl = ("http://free.currencyconverterapi.com/api/v5/"
                       "convert?q={}_UAH&compact=y")
        try:
            data_usd = requests.get(api_url_tpl.format('USD')).json()
            result['USD'] = data_usd['USD_UAH']['val']
            sleep(0.2)
            data_eur = requests.get(api_url_tpl.format('EUR')).json()
            result['EUR'] = data_eur['EUR_UAH']['val']
        except:
            return result
        return result
    
    def show(self):
        """ Show user information on display. """
        self.display.clean()
        self.display.font_set('NotoMono', self.font_size)
        # Show waiting icon.
        self.display.add_image_center('waiting.png')
        self.display.show()
        # Request rates.
        self.leds.blink('G')
        crypto_rates = self.get_cryptocurrencies_rates()
        self.leds.blink('G')
        uah_rates = self.get_usd_eur_rate()
        self.leds.blink('G')
        self.display.clean()
        # Draw cryptocurrncies rates.
        y = 0
        for i in range(0, len(crypto_rates)):
            line = "{} {}$ {}% 24h".format(
                crypto_rates[i]['name'], 
                int(float(crypto_rates[i]['price_usd'])), 
                crypto_rates[i]['percent_change_24h']
                )
            y = i * self.line_height
            self.display.add_text(line, x=0, y=y)
        # Draw USD->UAH and EUR->UAH rates.
        for rate in uah_rates:
            line = "{} = {} UAH".format(rate, uah_rates[rate])
            y += self.line_height
            self.display.add_text(line, x=0, y=y)
        # Show screen.
        self.display.show()