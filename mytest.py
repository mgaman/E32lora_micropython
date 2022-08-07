from machine import UART
from E32lora import E32lora
import time

'''
        E32 device             Pico      
         +----+              +---------+
     GND |    |--+ +---------| 15    16|
  +--VCC |    |  | | +-------| 14    17|  
  |      |    |  +-|-|-------| GND  GND|           
  |  AUX |    |----+ | +-----| 13    18|
  |  TX  |    |----+ | |  +--| 12    19|  Pin 12 open for transmit function
  |  RX  |    |--+ | | |  |  | 11    20|  to GND for receive function
  |  M1  |    |--|-|-+ |  |  | 10    21|
  |      |    |  | |   |  +--| GND  GND|  
  |  M0  |    |--|-|---+     | 9     22|
  |      +----+  | |         | 8       |
  |              | |         | 7     26|
  |              | |         | 6     27|
  |              | |         | GND  GND|  
  |              | +---------| 5     28|
  |              +-----------| 4       |
  |                          | 3    VCC|---+
  |                          | 2       |   |
  |                          | GND  GND|   |
  |                          | 1       |   |
  |                          | 0       |   |
  |                          +---------+   |
  |                                        |
  +----------------------------------------+

'''
def BroadcastTransparent():
    print('Broadcast Transparent')
    ser = UART(1,9600)
    lora = E32lora(ser,15,13,14)
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
        lora.sendFixedMessage(0xff,0xff,lora.config[4],line)
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

def test():
    print('test')

if __name__ == '__main__':
    test()
