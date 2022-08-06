from machine import UART
from E32lora import E32lora
import time

def BroadcastTransparent():
    print('Broadcast Transparent')
    ser = UART(1,9600)
    lora = E32lora(ser,15,13,14)
    lora.getModule()
    lora.setDebug(True)
    lora.getConfig()
    hostAddress = (lora.config[1],lora.config[2])
    lora.printConfig()
#    lora.setAddress((0,0))  # broadcaster must be 0x0000 or 0xFFFF
    lora.setAddress((0xff,0xff))  # broadcaster must be 0x0000 or 0xFFFF
    lora.setConfig(False)
    time.sleep(2)
    lora.getConfig()
    lora.printConfig()
    time.sleep(2)
    #lora.reset()
    count = 0
    while True:
        line = 'Broadcast Trans %d from %d:%d'%(count,hostAddress[0],hostAddress[1])
        #print(line)
        lora.sendMessage(line)
        count = count + 1
        time.sleep(2)

def Receiver():
    print('Receiver')
    ser = UART(1,9600)
    lora = E32lora(ser,15,13,14)
    lora.getModule()
    #lora.setDebug(True)
    lora.getConfig()
    # change channel to 1 if self address is 3
    lora.printConfig()
    # change channel to 1 if self address is 3
    if lora.config[1] == 0 and lora.config[2] == 3:
        lora.setChannel(1)
    lora.setFixedTransparent(False)
    lora.setConfig(False)
    lora.printConfig()
    lora.setMode(0)
    while True:
        d = lora.getData()
        if d is not None:
            print(d)


def BroadcastFixed():
    print('Broadcast Fixed')
    ser = UART(1,9600)
    lora = E32lora(ser,15,13,14)
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
        # now make a bytearray from addrh,addrl,channel and line
        ba = bytearray((0xff,0xff,lora.config[4]))+bytearray(line)
        lora.sendMessage(bytes(ba))
        count = count + 1
        time.sleep(2)

def TargetFixed():
    print('Target Fixed')
    ser = UART(1,9600)
    lora = E32lora(ser,15,13,14)
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
        ba=''
        if firstTarget:
            ba = bytearray((0,1,lora.config[4]))+bytearray(line)  # to 1 on same channel
        else:
            ba = bytearray((0,3,1))+bytearray(line)  # to 3 on different channel (1)
        firstTarget = not firstTarget
        lora.sendMessage(bytes(ba))
        count = count + 1
        time.sleep(2)

def test():
    print('test')

if __name__ == '__main__':
    test()
