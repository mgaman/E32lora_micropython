import sys
import time
from tests import BroadcastTransparent,Receiver,BroadcastFixed,TargetFixed
    
def getPythonType():
    global pythontype
    imptype = sys.implementation[0]
    print("Interpreter is",imptype)
    if  imptype == 'micropython':
        pythontype = 0
    elif imptype == 'circuitpython':
        pythontype = 1
    else:
        pythontype = -1
    return pythontype


if __name__ == '__main__':
    pythontype = -1
    choice = None
    choicevalue = None
    getPythonType()
    if pythontype == 0:
        from machine import Pin
        choice = Pin(12,Pin.IN,Pin.PULL_UP)
        choicevalue = choice.value()
    elif pythontype == 1:
        import board,digitalio
        choice = digitalio.DigitalInOut(board.GP16)
        choice.direction = digitalio.Direction.INPUT
        choice.pull = digitalio.Pull.UP
        choicevalue = choice.value

    if choicevalue == 1:           # pin not connected
        BroadcastTransparent()
        #BroadcastFixed()
        #TargetFixed()
    else:                             # pin to GND
        Receiver()

