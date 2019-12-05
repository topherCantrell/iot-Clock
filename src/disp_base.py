from abc import ABC, abstractmethod

class DisplayBase(ABC):
    
    @abstractmethod
    def get_window_size(self):
        pass
    
    @abstractmethod
    def make_time(self,oled,hours,minutes,seconds,is_pm):
        pass
    