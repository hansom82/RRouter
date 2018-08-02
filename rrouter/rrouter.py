#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# For more information see the README file.


""" Raspberry Pi Router/Server simple control script.
    v.1.0
"""


import os
import sys
import RPi.GPIO as GPIO

from daemonize import Daemonize
from random import choice
from subprocess import call
from time import sleep, time

import config
from beeper import Beeper
from display import Display
from leds import Leds
from menu import Menu
from sysinfo import SysInfo
from usrinfo import UsrInfo


PROGRAM_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'


class RRouter(object):
    """ Router controller program. """
    
    def __init__(self):
        self.pins = {}
        self.sounds_is_on = True
        self.animations_is_on = True
        self.animation_sets = []
        self.idle_time_to_sleep = 8
        self.oled_port = 1
        self.oled_i2c_address = 0x0
        self.images_path = ''
        
        self.sleeping = True
        self.last_key_press_time = 0
        
        self.wake_up_last_time = 0
        self.wake_up_timeout = 20
        
        self.inet_check_last_time = 0
        self.inet_check_timeout = 40
        self.inet_check_sound_notified = False
        
        self.oled = None
        self.menu = None
        self.beeper = None
        self.usrinfo = None
        self.sysinfo = None
        
    def prepare(self):
        """ Prepare environment. """
        # Prepare GPIO.
        GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            if self.pins[pin][1] == 'out':
                GPIO.setup(self.pins[pin][0], GPIO.OUT)
                GPIO.output(self.pins[pin][0], GPIO.HIGH)
            elif self.pins[pin][1] == 'in':
                GPIO.setup(self.pins[pin][0], GPIO.IN)
        # Initialize modules.
        self.oled = Display(port=self.oled_port, address=self.oled_i2c_address)
        self.oled.images_path = self.images_path
        self.menu = Menu(rr=self)
        self.beeper = Beeper(gpio=GPIO, speaker_pin=self.pins['Beeper'][0])
        self.beeper.mute = not self.sounds_is_on
        self.leds = Leds(gpio=GPIO, pins=self.pins)
        self.usrinfo = UsrInfo(display=self.oled, leds=self.leds)
        self.sysinfo = SysInfo(display=self.oled, leds=self.leds)
        # Set interrupts for buttons.
        for pin in self.pins:
            if 'BTN_' in pin:
                GPIO.add_event_detect( 
                    self.pins[pin][0], 
                    GPIO.FALLING, 
                    callback=self.button_pressed, 
                    bouncetime=100)
        
    def button_pressed(self, channel=0):
        """ Buttons actions. """
        # Get button name by it's channel.
        btn_name = ''
        for pin in self.pins:
            if self.pins[pin][0] == channel:
                btn_name = pin
                break
        if not btn_name:
            return False
        # Blink LED.
        self.leds.blink('B')
        # Play sound on button press.
        if btn_name in ['BTN_1', 'BTN_4', 'BTN_5']:
            self.beeper.play('alien-signal', length=1)
        else:
            self.beeper.play('click')
        # Actions for buttons.
        if btn_name == 'BTN_1':
            if self.sleeping:
                self.menu.show()
            else:
                # Menu items actions.
                if self.menu.selected_item == 1:
                    self.usrinfo.show() 
                elif self.menu.selected_item == 2:
                    self.sysinfo.show()
                elif self.menu.selected_item == 3:
                    if self.beeper.mute:
                        self.beeper.mute = False
                        self.show_image_center('sound-on.png')
                    else:    
                        self.beeper.mute = True
                        self.show_image_center('sound-off.png')
                elif self.menu.selected_item == 4:
                    if self.animations_is_on:
                        self.animations_is_on = False
                        self.show_image_center('animation-off.png')
                    else:
                        self.animations_is_on = True
                        self.show_image_center('animation-on.png')
                elif self.menu.selected_item == 5:
                    self.power_off()
        elif btn_name == 'BTN_2':
            self.menu.select_prev()
        elif btn_name == 'BTN_3':
            self.menu.select_next()
        elif btn_name == 'BTN_4':
            self.sysinfo.show()
        elif btn_name == 'BTN_5':
            self.usrinfo.show() 
        # Deactivate sleeping mode.
        self.sleeping = False
        self.last_key_press_time = time()
        
    def power_off(self):
        """ Powering OFF. """
        # Show message + simple countdown.
        self.leds.set_one('R', 1)
        self.oled.clean()
        self.oled.font_set('NotoMono', 17)
        self.oled.add_text('Powering OFF', x=0, y=21)
        self.oled.show()
        for i in range(0,8):
            x = i * 5
            self.oled.add_text('.', x=x, y=40)
            self.oled.show()
        # Shutdown.
        call('poweroff', shell=True)
    
    def show_animation(self, set_name='', repeat=1):
        """ Showing animation from PNG files. """
        set_prefix = 'anim_' + set_name
        files = []
        for f in os.listdir(self.images_path):
            if set_prefix in f \
            and os.path.isfile(os.path.join(self.images_path, f)):
                files.append(f)
        files.sort()
        for i in range(0, repeat):
            for img_file in files:
                self.show_image_center(img_file)
    
    def show_image_center(self, img_file=''):
        """ Show image in center of the screen. """
        self.oled.clean()
        self.oled.add_image_center(img_file)
        self.oled.show()
    
    def start(self):
        """ Main function for daemon. """
        # Main cycle.
        self.leds.set_all(1)
        self.show_animation('deb', repeat=2)
        self.leds.set_all(0)
        try:
            while True:
                # Sleeping mode guard.
                if self.last_key_press_time + self.idle_time_to_sleep < time():
                    self.sleeping = True
                    self.menu.selected_item = 0
                    self.oled.clean()
                    self.oled.show()
                # Wake UP + animations.
                if self.sleeping\
                   and self.wake_up_last_time + self.wake_up_timeout < time() \
                   and self.animations_is_on:
                    if self.wake_up_last_time:
                        self.show_animation(choice(self.animation_sets))
                    self.wake_up_last_time = time()
                # Internet connection checker.
                if self.sleeping\
                   and self.inet_check_last_time + \
                       self.inet_check_timeout < time():
                    if not self.sysinfo.check_host_port('8.8.8.8', 53):
                        self.leds.set_one('R', 1)
                        self.show_image_center('no-internet.png')
                        if not self.inet_check_sound_notified:
                            self.beeper.play('error')
                            self.inet_check_sound_notified = True
                    else:
                        self.leds.set_one('R', 0)
                        self.inet_check_sound_notified = False
                    self.inet_check_last_time = time()
                sleep(1)
        except KeyboardInterrupt:
            pass
        print('OK')
        GPIO.cleanup()
    

def main():
    """ Main function. """
    rr = RRouter()
    rr.pins = config.pins
    rr.oled_i2c_address = config.ssd1306_12c_address
    rr.sounds_is_on = config.sounds_is_on
    rr.aminations_is_on = config.aminations_is_on
    rr.animation_sets = config.animation_sets
    rr.idle_time_to_sleep = config.idle_time_to_sleep
    rr.images_path = PROGRAM_DIR + 'images/'
    rr.prepare()
    rr.start()

if len(sys.argv) == 2 and sys.argv[1] == '--manual':
    main()
else:
    # Give the time for netwirking to be UP.
    sleep(5)
    # Start as daemon.
    daemon = Daemonize(
        app="rrouter-daemon",
        pid='/tmp/rrouter-daemon.pid',
        action=main)
    daemon.start()


