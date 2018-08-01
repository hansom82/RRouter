# -*- coding: utf-8 -*-
#
# Copyright (c) 2018-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# For more information see the README file.


import os

from PIL import Image, ImageFont, ImageDraw
from ssd1306 import ssd1306, const


class Display(object):
    """ Class for working with OLED display. """
    
    def __init__(self, port=1, address=0x3C):
        self.fonts = {
            'NotoMono' : '/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf'
            }
        self.images_path = ''
        self.font = ImageFont.load_default()
        self.oled = ssd1306(port, address)
        self.oled.command(const.SETCONTRAST)
        self.oled.command(128)
        self.image = Image.new('1', (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)
        
    def font_set(self, font_name='', font_size=10):
        """ Set current font name. """
        if font_name not in self.fonts.keys():
            print("ERROR: Font '{}' not defined!".format(font_name))
            return False
        self.font = ImageFont.truetype(self.fonts[font_name], font_size)
    
    def add_text(self, text='', x=0, y=0):
        """ Draw text. """
        self.draw.text((x, y), text, font=self.font, fill=255)
    
    def open_image(self, file_name=''):
        """ Open image to work with. """
        img_path = self.images_path + file_name
        if not os.path.isfile(img_path):
            return False
        return Image.open(img_path).convert('L')
    
    def add_image(self, file_name='', x=0, y=0):
        """ Draw image. """
        pic = self.open_image(file_name)
        self.draw.bitmap((x, y), pic, fill=255)
        
    def add_image_center(self, file_name='', rotate_angle=0):
        """ Draw image in center. """
        pic = self.open_image(file_name)
        if rotate_angle:
            pic.rotate(rotate_angle)
        width, height = pic.size
        x = int((self.oled.width - width) / 2)
        y = int((self.oled.height - height) / 2)
        self.draw.bitmap((x, y), pic, fill=255)
        
    def clean(self):
        """ Clean display. """
        self.draw.rectangle((
            0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
    
    def show(self):
        """ Showing prepared data on display. """
        self.oled.display(self.image)

