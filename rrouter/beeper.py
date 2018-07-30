# -*- coding: utf-8 -*-
#
# Copyright (c) 2018-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# For more information see the README file.


import RPi.GPIO as GPIO
from random import randrange
from time import sleep, time


class Beeper(object):
    """ Class for playing sounds via Buzzer. """
    
    def __init__(self, gpio=None, speaker_pin=0):
        self.gpio = gpio
        self.speaker_pin = speaker_pin
        self.mute = False
        
        self.start_time = 0
        
    def sound_alien(self, length_sec=0):
        """ Play 'aliens signal' sound :) """
        pwm = self.gpio.PWM(self.speaker_pin, 1)
        pwm.start(50)
        while True:
            pwm.ChangeFrequency(randrange(20,10001))
            sleep(randrange(1,5)/100)
            if self.start_time + length_sec < time():
                break
        pwm.stop()
    
    def sound_click(self):
        """ Play 'click' sound. """
        for i in range(0,2):
            self.gpio.output(self.speaker_pin, GPIO.HIGH)
            sleep(0.001)
            self.gpio.output(self.speaker_pin, GPIO.LOW)
            sleep(0.002)

    def sound_error(self):
        """ Play 'error' sound. """
        for i in range(0,8):
            self.gpio.output(self.speaker_pin, GPIO.HIGH)
            sleep(0.002)
            self.gpio.output(self.speaker_pin, GPIO.LOW)
            sleep(0.004)
         
    def play(self, sound_name='', length=0):
        """ Play specified sound template. """
        if not self.speaker_pin or self.mute:
            return False
        self.start_time = time()
        if sound_name == 'alien-signal':
            self.sound_alien(length)
        elif sound_name == 'click':
            self.sound_click()
        elif sound_name == 'error':
            self.sound_error()