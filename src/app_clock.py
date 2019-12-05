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

from disp_large7seg import Large7SegDisplay

import RPi.GPIO as GPIO

# Button
PIN_BUTTON = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.input(PIN_BUTTON)

# The OLED hardware driver
oled = OLED()
window = OLEDWindow(oled,0,0,256,64)

displays = [
    Large7SegDisplay(window),
]

xofs = -1
yofs = -1
dirx = 1
diry = 1
display = None
    
def set_display(num):
    global xofs,yofs,dirx,diry,display
    display = displays[num]    

display_ptr = 0
set_display(display_ptr)

# TODO: different screen-saver algorithms

# TODO: pick a display implementation (button press)
# TODO: press button to show info (IP address)

while True:
    
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
                    
    # Sleep loop 0.1 sec here and watch button
    time.sleep(10)        
    
