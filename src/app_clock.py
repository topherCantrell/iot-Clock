"""
 - Add this line to /etc/rc.local (before the exit 0):
  -   /home/pi/ONBOOT.sh 2> /home/pi/ONBOOT.errors > /home/pi/ONBOOT.stdout &
  - Add the following ONBOOT.sh script to /home/pi and make it executable:
  
#!/bin/bash
cd /home/pi/iot-clock/src
python app_clock.py
"""

import datetime
import os
import time

import tornado.ioloop
import tornado.web

import RPi.GPIO as GPIO
from disp_large7seg import Large7SegDisplay
from disp_place_holder import PlaceHolder
from oled.oled_pi import OLED
from oled.oled_window import OLEDWindow

# Singleton clock controller
CLOCK = None


class Clock:

    def __init__(self, window, displays, config):
        self._window = window
        self._displays = displays
        self._xofs = -1
        self._yofs = -1
        self._dirx = 1
        self._diry = 1
        self._config = config

    def button_pressed_cb(self):
        self.set_display()

    def get_config(self):
        return self._config

    def set_display(self, num=-1):
        if num >= 0:
            self._display_ptr = num
        else:
            self._display_ptr += 1
            if self._display_ptr >= len(self._displays):
                self._display_ptr = 0
        self.update_time()

    def update_time(self):
        window_size = self._display.get_window_size()
        limits = [256 - window_size[0], 64 - window_size[1]]

        self._xofs += self._dirx
        if self._xofs > limits[0]:
            self._xofs = limits[0]
            self._dirx = -1
        if self._xofs < 0:
            self._xofs = 0
            self._dirx = 1

        self._yofs += self._diry
        if self._yofs > limits[1]:
            self._yofs = limits[1]
            self._diry = -1
        if self._yofs < 0:
            self._yofs = 0
            self._diry = 1

        now = datetime.datetime.now()

        hours = now.hour
        mins = now.minute
        secs = now.second

        self._window.clear()
        self._display.make_time(self._xofs, self._yofs, hours, mins, secs, self._config)
        self._window.draw_screen_buffer()


class ClockHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello")
        # Return JSON: brightness, list-of-displays, current-display

    def post(self):
        global second_count, display, display_ptr
        self.write("HelloPost")
        # Brightnes, current-display
        second_count = 99
        tornado.ioloop.IOLoop.current().call_later(delay=0.1, callback=tenth_second)


if __name__ == '__main__':

    # The OLED hardware driver
    oled = OLED()
    window = OLEDWindow(oled, 0, 0, 256, 64)

    displays = [
        Large7SegDisplay(window),
        PlaceHolder(window, 'Binary'),
        PlaceHolder(window, 'Analog'),
        PlaceHolder(window, 'Analog Roman'),
        PlaceHolder(window, 'Tetris'),
        PlaceHolder(window, 'Simple Text'),
        PlaceHolder(window, 'Word'),
    ]

    # TODO: this should persist in a config file
    config = {
        brightness: 15,
        am_pm: True,
        display_num: 0
    }

    clock = Clock(window, displays, config)

    # Make sure the button handler runs in the tornando I/O loop
    def _button_handler(_channel):
        tornado.ioloop.IOLoop.current().add_callback(CLOCK.button_pressed_cb)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(23, GPIO.RISING, callback=_button_handler, bouncetime=200)

    root = os.path.join(os.path.dirname(__file__), "webroot")
    handlers = [
        (r"/cgi/(.*)", ClockHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": root, "default_filename": "index.html"}),
    ]

    app = tornado.web.Application(handlers)
    app.listen(80)

    # Every 10 seconds, update the display
    def _time_change():
        CLOCK.update_time()
        tornado.ioloop.IOLoop.current().call_later(10, _time_change)
    time_change()

    tornado.ioloop.IOLoop.current().start()
