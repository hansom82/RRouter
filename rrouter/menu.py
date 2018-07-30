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


class Menu(object):
    """ Class for rendering menu. """
    
    def __init__(self, rr=None):
        self.rr = rr
        self.line_height = 10
        self.selected_item = 0
    
    def select_next(self):
        """ Select next item. """
        item_max = len(self.menu_lines)
        self.selected_item += 1
        if self.selected_item > item_max:
            self.selected_item = item_max
        self.show()
            
    def select_prev(self):
        """ Select previous item. """
        self.selected_item -= 1
        if self.selected_item <=0:
            self.selected_item = 1
        self.show()
    
    def show(self):
        """ Show prepared menu. """
        self.menu_lines = [
            "1. Show USER info",
            "2. Show SYSTEM info",
            "3. Set BEEPER {}".format('OFF' if self.rr.sounds_is_on else 'ON'),
            "4. Set ANIMATIONS {}".format(
                'OFF' if self.rr.animations_is_on else 'ON'
                ),
            "5. POWER OFF",
            ]
        items_count = len(self.menu_lines)
        if not items_count:
            return False
        self.rr.oled.clean()
        self.rr.oled.font_set('NotoMono', self.line_height)
        y = 1
        for i in range(0, items_count):
            line = self.menu_lines[i]
            if self.selected_item and self.selected_item == i+1:
                line = re.sub(r'^[0-9\.]{2}', '->', line)
            self.rr.oled.add_text(line, x=0, y=y)
            y += self.line_height + 2
        self.rr.oled.show()
        return True