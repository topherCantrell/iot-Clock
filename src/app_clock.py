"""
 - Add this line to /etc/rc.local (before the exit 0):
  -   /home/pi/ONBOOT.sh 2> /home/pi/ONBOOT.errors > /home/pi/ONBOOT.stdout &
  - Add the following ONBOOT.sh script to /home/pi and make it executable:
  
#!/bin/bash
cd /home/pi/iot-clock/src
python app_clock.py
"""

# Maybe blink the colon ever so often to show running

from OLED import OLED
from OLEDWindow import OLEDWindow
import time
import datetime

# Button
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.input(23)

DIGIT_OFS = [
    [29-5,0],
    [81-5,0],
    [143-5,0],
    [195-5,0]
    ]

COLON_OFS = [
    [126-5,16],
    [126-5,42]
    ]

SEVEN_SEGS = [
    'abcdef', # 0
    'bc', # 1
    'abdeg', # 2
    'abcdg', # 3
    'bcfg', # 4
    'acdfg', # 5
    'acdefg', # 6
    'abc', # 7
    'abcdefg', # 8
    'abcdfg', # 9
    ]

def draw_colon():
    for num in range(2):
        x = COLON_OFS[num][0]
        y = COLON_OFS[num][1]
        window_one.DrawBox(x,y,5,5,8)
        
def draw_digit(num,value):
    
    # clockwise from top: a,b,c,d,e,f, and g in middle
    
    segs = SEVEN_SEGS[value]
        
    x = DIGIT_OFS[num][0]
    y = DIGIT_OFS[num][1]

    if 'a' in segs: window_one.DrawBox(x+0,y+2,32,6,15) # a    
    if 'b' in segs: window_one.DrawBox(x+28,y+2,5,32,15) # b
    if 'c' in segs: window_one.DrawBox(x+28,y+29,5,32,15) # c
    if 'd' in segs: window_one.DrawBox(x+0,y+56,32,5,15) # d
    if 'e' in segs: window_one.DrawBox(x+0,y+29,5,32,15) # e
    if 'f' in segs: window_one.DrawBox(x+0,y+2,5,32,15) # f
    if 'g' in segs: window_one.DrawBox(x+0,y+29,32,5,15) # g
    
# The OLED hardware driver
oled = OLED()

window_one = OLEDWindow(oled,0,0,256,64)

while True:

    window_one.clear()
    draw_colon()
    
    now = datetime.datetime.now()    
    hours = now.hour
    mins = now.minute
    pm = False
    if hours>12:
        hours = hours - 12
        pm = True
    
    hours_a = int(hours/10)
    hours_b = int(hours%10)
    mins_a = int(mins/10)
    mins_b = int(mins%10)

    if hours_a>0:
        draw_digit(0,hours_a)
    draw_digit(1,hours_b)
    draw_digit(2,mins_a)
    draw_digit(3,mins_b)
    
    if pm:
        window_one.draw_big_text(232,47,"PM",8,14)

    window_one.draw_screen_buffer()
    
    time.sleep(10)

