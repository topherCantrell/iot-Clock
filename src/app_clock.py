"""
 - Add this line to /etc/rc.local (before the exit 0):
  -   /home/pi/ONBOOT.sh 2> /home/pi/ONBOOT.errors > /home/pi/ONBOOT.stdout &
  - Add the following ONBOOT.sh script to /home/pi and make it executable:
  
#!/bin/bash
cd /home/pi/iot-clock/src
python app_clock.py
"""

# Maybe blink the colon ever so often to show running

# 0,0 .. 124,25

from oled.oled_pi import OLED
from oled.oled_window import OLEDWindow
import time
import datetime

import tornado.ioloop
import tornado.web
import os

from disp_large7seg import Large7SegDisplay
from disp_place_holder import PlaceHolder

import RPi.GPIO as GPIO

# Button
PIN_BUTTON = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_state = GPIO.input(PIN_BUTTON)

# The OLED hardware driver
oled = OLED()
window = OLEDWindow(oled,0,0,256,64)

displays = [
    Large7SegDisplay(window),
    PlaceHolder(window,'Binary'),
    PlaceHolder(window,'Analog'),
    PlaceHolder(window,'Tetris'),
    PlaceHolder(window,'Roman'),
    PlaceHolder(window,'Text'),
    PlaceHolder(window,'Word'),    
]

xofs = -1
yofs = -1
dirx = 1
diry = 1
display = None

display_ptr = 0
display = displays[display_ptr]

second_count = 99

def button_pressed(channel):
    print('HERE')
    
GPIO.add_event_detect(PIN_BUTTON,GPIO.RISING,callback=button_pressed,bouncetime=200)

def set_display_ptr(num=-1):
    global second_count,button_state,display_ptr,display    
    if num>=0:
        display_ptr = num
    else:
        display_ptr +=1     
        if display_ptr>=len(displays):
            display_ptr = 0
    second_count = 99
    display = displays[display_ptr]   

def tenth_second():
    global second_count,button_state
    
    bs = GPIO.input(PIN_BUTTON)    
    if bs != button_state:
        button_state = bs
        if not bs:
            set_display_ptr()
    
    second_count+=1
    if second_count>=100:
        second_count = 0
        ten_second()
    tornado.ioloop.IOLoop.current().call_later(delay=0.1,callback=tenth_second)

def ten_second():
    global xofs, yofs, dirx, diry, display
        
    window_size = display.get_window_size()
    limits = [256-window_size[0],64-window_size[1]]
    
    xofs = xofs + dirx
    if xofs>limits[0]:
        xofs = limits[0]
        dirx = -1
    if xofs<0:
        xofs = 0
        dirx = 1
        
    yofs = yofs + diry
    if yofs>limits[1]:
        yofs = limits[1]
        diry = -1
    if yofs<0:
        yofs = 0
        diry = 1
        
    now = datetime.datetime.now()    
     
    hours = now.hour
    mins = now.minute
    secs = now.second
    
    window.clear()        
    display.make_time(xofs,yofs,hours,mins,secs,True)
    window.draw_screen_buffer()


class ClockHandler(tornado.web.RequestHandler):
    
    def get(self):               
        self.write("Hello")
        # Return JSON: brightness, list-of-displays, current-display
        
    def post(self):  
        global second_count,display,display_ptr
        self.write("HelloPost")      
        # Brightnes, current-display
        second_count = 99
        tornado.ioloop.IOLoop.current().call_later(delay=0.1,callback=tenth_second) 
  
root = os.path.join(os.path.dirname(__file__), "webroot")

handlers = [
    (r"/cgi/(.*)", ClockHandler),        
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": root, "default_filename": "index.html"}),
    ]

app = tornado.web.Application(handlers)
app.listen(80)
tenth_second()
tornado.ioloop.IOLoop.current().start()

