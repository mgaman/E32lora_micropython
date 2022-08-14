import sys
import time
from E32lora import E32lora

pythontype = -1
    
def getPythonType():
    global pythontype
    imptype = sys.implementation[0]
    if  imptype == 'micropython':
        pythontype = 0
    elif imptype == 'circuitpython':
        pythontype = 1
    else:
        pythontype = -1
    return pythontype
    
def Receiver():
    global pythontype
    print('Receiver')
    getPythonType()
    if pythontype == 0:
        from machine import UART
    else:
        from busio import UART
        import board
    #createLora()
    if pythontype == 0:
        ser = UART(1,9600)
        lora = E32lora(ser,15,13,14)
    else:
        ser = UART(board.GP4,board.GP5,baudrate=9600,receiver_buffer_size=64)
        lora = E32lora(ser,board.GP17,board.GP2,board.GP3)
    lora.getModule()
    lora.getConfig()
    lora.printConfig()
    lora.setChannel(23)
    lora.setFixedTransparent(False)
    lora.setConfig(False)
    lora.printConfig()
    lora.setMode(0)
    while True:
        d = lora.getData()
        if d is None:
            pass
        else:
            print(d)

def BroadcastTransparent():
    global pythontype
    print('Broadcast Transparent')
    getPythonType()
    if pythontype == 0:
        from machine import UART
    else:
        from busio import UART
        import board
    #createLora()
    if pythontype == 0:
        ser = UART(1,9600)
        lora = E32lora(ser,15,13,14)
    else:
        ser = UART(board.GP4,board.GP5,baudrate=9600,receiver_buffer_size=64)
        lora = E32lora(ser,board.GP17,board.GP2,board.GP3)
    lora.getModule()
    lora.setDebug(True)
    lora.getConfig()
    hostAddress = (lora.config[1],lora.config[2])
    lora.printConfig()
    lora.setAddress(0xff,0xff)  # broadcaster must be 0xffff
    lora.setFixedTransparent(False)
    lora.setConfig(False)
    time.sleep(2)
    lora.getConfig()
    lora.printConfig()
    time.sleep(2)
    #lora.reset()
    count = 0
    while True:
        line = 'Broadcast Transparent %d from %d:%d'%(count,hostAddress[0],hostAddress[1])
        #print(line)
        lora.sendTransparentMessage(line)
        count = count + 1
        time.sleep(2)

def BroadcastFixed():
    global pythontype
    print('Broadcast Fixed')
    getPythonType()
    if pythontype == 0:
        from machine import UART
    else:
        from busio import UART
        import board
    #createLora()
    if pythontype == 0:
        ser = UART(1,9600)
        lora = E32lora(ser,15,13,14)
    else:
        ser = UART(board.GP4,board.GP5,baudrate=9600,receiver_buffer_size=64)
        lora = E32lora(ser,board.GP17,board.GP2,board.GP3)
    lora.getModule()
    lora.setDebug(True)
    lora.getConfig()
    hostAddress = (lora.config[1],lora.config[2])
    lora.printConfig()
    lora.setFixedTransparent(True)  # set fixed mode
    lora.setConfig(False)
    time.sleep(2)
    lora.getConfig()
    lora.printConfig()
    time.sleep(2)
    count = 0
    while True:
        line = 'Broadcast Fixed %d from %d:%d'%(count,hostAddress[0],hostAddress[1])
        lora.sendFixedMessage(0xff,0xff,lora.config[4],line)
        count = count + 1
        time.sleep(2)

def TargetFixed():
    global pythontype
    print('Target Fixed')
    getPythonType()
    if pythontype == 0:
        from machine import UART
    else:
        from busio import UART
        import board
    #createLora()
    if pythontype == 0:
        ser = UART(1,9600)
        lora = E32lora(ser,15,13,14)
    else:
        ser = UART(board.GP4,board.GP5,baudrate=9600,receiver_buffer_size=64)
        lora = E32lora(ser,board.GP17,board.GP2,board.GP3)
    lora.getModule()
    lora.setDebug(True)
    lora.getConfig()
    hostAddress = (lora.config[1],lora.config[2])
    lora.printConfig()
    lora.setFixedTransparent(True)  # set fixed mode
    lora.setConfig(False)
    time.sleep(2)
    lora.getConfig()
    lora.printConfig()
    time.sleep(2)
    count = 0
    firstTarget = True  # used to swap between 2 targets
    # should see every other message appearing at target
    while True:
        line = 'Target Fixed %d from %d:%d'%(count,hostAddress[0],hostAddress[1])
        # now make a bytearray from addrh,addrl,channel and line
        addh=0
        addl=0
        ch=lora.config[4]
        if firstTarget:
            addl = 1
        else:
            addl = 3
            ch = 1
        lora.sendFixedMessage(addh,addl,ch,line)
        firstTarget = not firstTarget
        count = count + 1
        time.sleep(2)
