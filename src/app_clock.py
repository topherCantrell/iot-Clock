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

from OLED import OLED
from OLEDWindow import OLEDWindow
import time
import datetime

# Button
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.input(23)

LIMITS = [124,24]

SEG_LENGTH = 18
SEG_WIDTH = 3
SEG_COLOR = 15

COLON_SIZE = 3
COLON_COLOR = 8

PM_X = (SEG_LENGTH+SEG_LENGTH+10)*2+27
PM_Y = SEG_LENGTH*2 - 5
PM_COLOR = 15

DIGIT_OFS = [
    [0,0],
    [SEG_LENGTH+10,0],
    [(SEG_LENGTH+10)*2+9,0],
    [(SEG_LENGTH+10)*3+9,0]
    ]

COLON_OFS = [
    [(SEG_LENGTH+8)*2+4,int(SEG_LENGTH/2)+2],
    [(SEG_LENGTH+8)*2+4,SEG_LENGTH+int(SEG_LENGTH/2)]
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

def draw_colon(xofs,yofs):
    for num in range(2):
        x = COLON_OFS[num][0]
        y = COLON_OFS[num][1]
        window_one.DrawBox(x+xofs,y+yofs,COLON_SIZE,COLON_SIZE,COLON_COLOR)
        
def draw_digit(xofs,yofs,num,value):
    
    # clockwise from top: a,b,c,d,e,f, and g in middle
    
    segs = SEVEN_SEGS[value]
        
    x = DIGIT_OFS[num][0]
    y = DIGIT_OFS[num][1]

    if 'a' in segs: window_one.DrawBox(x+xofs+1, y+yofs+0,                       SEG_LENGTH, SEG_WIDTH,  SEG_COLOR) # a    
    if 'b' in segs: window_one.DrawBox(x+xofs+SEG_LENGTH-1, y+yofs+1,            SEG_WIDTH,  SEG_LENGTH, SEG_COLOR) # b
    if 'c' in segs: window_one.DrawBox(x+xofs+SEG_LENGTH-1, y+yofs+SEG_LENGTH+2, SEG_WIDTH,  SEG_LENGTH, SEG_COLOR) # c
    if 'd' in segs: window_one.DrawBox(x+xofs+1, y+yofs+SEG_LENGTH*2,            SEG_LENGTH, SEG_WIDTH,  SEG_COLOR) # d
    if 'e' in segs: window_one.DrawBox(x+xofs+0, y+yofs+SEG_LENGTH+2,            SEG_WIDTH,  SEG_LENGTH, SEG_COLOR) # e
    if 'f' in segs: window_one.DrawBox(x+xofs+0, y+yofs+1,                       SEG_WIDTH,  SEG_LENGTH, SEG_COLOR) # f
    if 'g' in segs: window_one.DrawBox(x+xofs+1, y+yofs+SEG_LENGTH,              SEG_LENGTH, SEG_WIDTH,  SEG_COLOR) # g
    
# The OLED hardware driver
oled = OLED()

window_one = OLEDWindow(oled,0,0,256,64)
xofs = 0
yofs = 0
dirx = 1
diry = 1

while True:
        
    window_one.clear()
    draw_colon(xofs,yofs)
    
    now = datetime.datetime.now()    
    hours = now.hour
    mins = now.minute
    pm = False
    if hours>12:
        hours = hours - 12
        pm = True    
    
    hours_a = int(hours/10)
    hours_b = int(hours%10)
    mins_a =  int(mins/10)
    mins_b =  int(mins%10)

    if hours_a>0:
        draw_digit(xofs,yofs,0,hours_a)
    draw_digit(xofs,yofs,1,hours_b)
    draw_digit(xofs,yofs,2,mins_a)
    draw_digit(xofs,yofs,3,mins_b)
    
    if pm:
        window_one.draw_text(PM_X+xofs,PM_Y+yofs,'PM',PM_COLOR)

    window_one.draw_screen_buffer()
    
    time.sleep(10)    
    
    xofs = xofs + dirx
    if xofs>LIMITS[0]:
        xofs = LIMITS[0]
        dirx = -1
    if xofs<0:
        xofs = 0
        dirx = 1
        
    yofs = yofs + diry
    if yofs>LIMITS[1]:
        yofs = LIMITS[1]
        diry = -1
    if yofs<0:
        yofs = 0
        diry = 1
