# -*- coding: utf-8 -*-
#
# Copyright (c) 2018-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# For more information see the README file.


from time import sleep


class Leds(object):
    """ Switching leds. """
    
    def __init__(self, gpio=None, pins=None):
        self.pins = pins
        self.gpio = gpio
    
    def set_one(self, name='R', state=True):
        """ Set LEDs state ON/OFF. """
        try:
            pin = self.pins['LED_{}'.format(name)][0]
        except:
            return False
        if state:
            self.gpio.output(pin, self.gpio.LOW)
        else:
            self.gpio.output(pin, self.gpio.HIGH)
    
    def set_all(self, leds_val={'R':0, 'G':0, 'B':0}):
        """ Set all leds state. """
        if leds_val == 1 or leds_val == 0:
            for led in ['R', 'G', 'B']:
                self.set_one(led, leds_val)
        elif len(leds_val):
            for led in leds_val:
                self.set_one(led, leds_val[led])
    
    def blink(self, name='R'):
        """ Blink one LED. """
        self.set_one(name, 1)
        sleep(0.1)
        self.set_one(name, 0)
