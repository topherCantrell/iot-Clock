from disp_base import DisplayBase

class PlaceHolder(DisplayBase):
    
    def __init__(self,window,text):
        self._window = window
        self._text = text
        
    def get_window_size(self):
        return (128,40)
    
    def make_time(self,xofs,yofs,hours,minutes,_seconds,_is_am_pm):
        self._window.draw_big_text(xofs+5,yofs+4,self._text,15)
        ts = str(hours)
        ms = str(minutes)
        if len(ms)<2:
            ms = '0'+ms
        self._window.draw_big_text(xofs+5,yofs+22,ts+':'+ms,15)
        
        