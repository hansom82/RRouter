# -*- coding: utf-8 -*-
#
# Copyright (c) 2018-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# For more information see the README file.


import re
import socket

from subprocess import Popen, PIPE
from time import time, strftime, localtime


class SysInfo(object):
    """ Collecting and showing system information. """
    
    def __init__(self, display=None, leds=None):
        self.display = display
        self.leds = leds
        
        self.line_height = 11
        self.font_size = 10

    def get_cmd_output(self, command=''):
        """ Rin command and capture it's output. """
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        if process.returncode:
            return False
        return out.decode("utf-8") 

    def temperature_format(self, string=''):
        """ Format temperature string like '35011'. """
        return '{:.2f}'.format(int(string) / 1000)
        
    def cpu_temperature(self):
        """ Get CPU temperature. """
        out = self.get_cmd_output('cat /sys/class/thermal/thermal_zone0/temp')
        match = re.match(r'^[0-9]+', out)
        if not match:
            return 0
        return self.temperature_format(match.group())
    
    def box_temperature(self):
        """ Get BOX temperature using DS18B20 1-Wire sensor. """
        # Get list of 1-Wire devices found.
        out = self.get_cmd_output('ls /sys/bus/w1/devices/')
        match = re.match(r'28\-[0-9a-z]+', out)
        if not match:
            return 0
        sensor_id = match.group()
        cmd = 'cat /sys/bus/w1/devices/{}/w1_slave'.format(sensor_id)
        out = self.get_cmd_output(cmd)
        match = re.search(r't=[0-9]+', out, re.MULTILINE)
        if not match:
            return 0
        return self.temperature_format(match.group().strip('t='))
    
    def memory(self):
        """ Get memory load. """
        result = {'Total': 0, 'Used': 0, 'Free': 0}
        out = self.get_cmd_output('free -tm')
        match = re.search(r'^Total:\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)', out, re.MULTILINE)
        if not match:
            return result
        return {
            'Total': match.groups()[0], 
            'Used': match.groups()[1], 
            'Free': match.groups()[2]
            }
        
    def check_host_port(self, host='8.8.8.8', port=53, timeout=2):
        """ Check if host's port is opened. """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM)\
                .connect((host, port))
            return True
        except:
            return False
        
    def show(self):
        """ Show system information on display. """
        self.display.clean()
        self.display.font_set('NotoMono', self.font_size)
        # Show gears icon.
        self.display.add_image_center('gears.png')
        self.display.show()
        # Gather sysinfo.
        datetime = strftime("%d-%m-%Y %H:%M", localtime(time()))
        self.leds.blink('G')
        cpu_temp = self.cpu_temperature()
        self.leds.blink('G')
        box_temp = self.box_temperature()
        self.leds.blink('G')
        inet_ok = self.check_host_port('8.8.8.8', 53, 3)
        self.leds.blink('G')
        memory = self.memory()
        self.leds.blink('G')
        # show info.
        lines = [
            '{}'.format(datetime),
            '------------------------',
            'CPU temp: {} °C'.format(cpu_temp),
            'BOX temp: {} °C'.format(box_temp),
            'MEM: {} M / {} M'.format(memory['Used'], memory['Total']),
            'INTERNET: {}'.format('ok' if inet_ok else 'error'),
            ]
        self.display.clean()
        for i in range(0, len(lines)):
            y = i * self.line_height
            self.display.add_text(lines[i], x=0, y=y)
        self.display.show()
        
        
        
        
        