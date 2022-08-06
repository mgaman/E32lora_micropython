from mytest import BroadcastTransparent,Receiver,BroadcastFixed,TargetFixed
from machine import Pin

if __name__ == '__main__':
    choice = Pin(12,Pin.IN,Pin.PULL_UP)
    if choice.value() == 1:
        #BroadcastTransparent()
        #BroadcastFixed()
        TargetFixed()
    else:
        Receiver()


