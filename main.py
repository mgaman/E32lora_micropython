from mytest import BroadcastTransparent,Receiver,BroadcastFixed,TargetFixed
from machine import Pin

if __name__ == '__main__':
    choice = Pin(12,Pin.IN,Pin.PULL_UP)
    if choice.value() == 1:           # pin not connected
        #BroadcastTransparent()
        #BroadcastFixed()
        TargetFixed()
    else:                             # pin to GND
        Receiver()


