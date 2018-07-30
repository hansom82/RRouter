# -*- coding: utf-8 -*-
#
# Copyright (c) 2018-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# For more information see the README file.


# GPIO pins configuration (BCM).
pins = {
    'Beeper':  [18, 'out'],
    'LED_R':   [23, 'out'],
    'LED_G':   [24, 'out'],
    'LED_B':   [25, 'out'],
    'BTN_1':   [21, 'in'],
    'BTN_2':   [16, 'in'],
    'BTN_3':   [12, 'in'],
    'BTN_4':   [20, 'in'],
    'BTN_5':   [7,  'in'],
    }

# Display I2C address.
ssd1306_12c_address = 0x3C

# 1 = ON, 0 = OFF.
sounds_is_on = 1
aminations_is_on = 1
animation_sets = ['deb', 'atom', 'cat']
# Time in seconds from the last key press after which menu will hide.
idle_time_to_sleep = 20
