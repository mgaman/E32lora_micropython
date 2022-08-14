import time
import sys    
class E32lora:
    """
    Written for the E32900T20D device. I assume that all the code is relevant to other
    E32T*** modules except that relating to the power setting in the Config section
    It is required to connect all the pins (AUX,M0,M1). 
    """
    '''
    class Parity(Enum):
        P8N1 = 0,
        P801 = 1,
        P8E1 = 2

    class BaudRate(Enum):
        B1200 = 0,
        B2400 = 1,
        B4800 = 2,
        B9600 = 3,
        B19200 = 4,
        B38400 = 5,
        B57600 = 6,
        B115200 = 7

    class AirRate(Enum):
        AR300 = 0,
        AR1200 = 1,
        AR2400 = 2,
        AR4800 = 3,
        AR9600 = 5,
        AR19200 = 5

    class WakeupTime(Enum):
        WU250 = 0,
        WU500 = 1,
        WU750 = 2,
        WU1000 = 3,
        WU1250 = 4,
        WU1500 = 5,
        WU1750 = 6,
        WU2000 = 7

    class Power(Enum):
        DBM20 = 0,
        DBM17 = 1,
        DBM14 = 2,
        DBM10 = 3
        
    class Mode(Enum):
        MODE_NORMAL = 0,
        MODE_WAKEUP = 1,
        MODE_POWERSAVE = 2,
        MODE_SLEEP = 3
'''
    def __init__(self,serial,aux,m0,m1):
        """
        Constructor
        @parameter Serial. A UART object created by the invoker
        @parameter aux. The GPIO pin number of AUX
        @parameter m0. The GPIO pin number of M0
        @parameter m1. The GPIO pin number of M1
        """
        self.getPythonType()
        if self.pythontype == 0:   #micropython
            from machine import Pin,UART
        elif self.pythontype == 1: #circuitpython
            import board
            import digitalio
            import busio
            
        self.serial = serial
        if self.pythontype == 0:
            self.aux = Pin(aux,Pin.IN,Pin.PULL_UP)
            self.m0 = Pin(m0,Pin.OUT)
            self.m1 = Pin(m1,Pin.OUT)
            self.m0.low()
            self.m1.low()
        elif self.pythontype == 1:
            self.aux = digitalio.DigitalInOut(aux)
            self.aux.direction = digitalio.Direction.INPUT
            self.aux.pull = digitalio.Pull.UP
            self.m0 = digitalio.DigitalInOut(m0)
            self.m0.direction = digitalio.Direction.OUTPUT
            self.m0.value = 0
            self.m1 = digitalio.DigitalInOut(m1)
            self.m1.direction = digitalio.Direction.OUTPUT
            self.m1.value = 0
            
        self.mode = 0
        self.paritytypes = ['Parity 8N1 (default)','Parity 8O1','Parity 8E1','Parity 8N1']
        self.baudtypes = ['UART baudrate 1200bps','UART baudrate 2400bps','UART baudrate 4800bps',
              'UART baudrate 9600bps (default)','UART baudrate 19200bps','UART baudrate 38400bps',
              'UART baudrate 57600bps','UART baudrate 115200bps']
        self.ratetypes = ['air rate 0.3K','air rate 1.2K','air rate 2.4K (default)','air rate 4.8K',
                        'air rate 9.6K','air rate 19.2K','air rate 19.2K','air rate 19.2K']
        self.waketypes=['Wakeup time 250ms (default)','Wakeup time 500ms','Wakeup time 750ms','Wakeup time 1000ms',
                        'Wakeup time 1250ms','Wakeup time 1500ms','Wakeup time 1750ms','Wakeup time 2000ms']
        self.powertypes = ['power 20dBm (default)','power 17dBm','power 14dBm','power 10dBm']
        self.haveconfig = False
        self.debug = False

    def getPythonType(self):
        imptype = sys.implementation[0]
        #print(imptype)
        if  imptype == 'micropython':
            self.pythontype = 0
        elif imptype == 'circuitpython':
            self.pythontype = 1
        else:
            self.pythontype = -1
        return self.pythontype

    def getVersion(self):
            #return '0.1'   # initial working version, time.sleep instead of AUX
            #return '0.2'   # replace sendMessage by sendTransparentMessage and sendFixedMessage
            #return '0.3'    # tweak the use of AUX
            return '0.4'    # added circuitpython support  

    def setDebug(self,flag):
        """
        Turn debugging messages on or off
        @parameter flag True to turn on messages, else False
        """
        self.debug = flag 

    def setMode(self,mode):
        """
        Set the operating mode
        @parameter mode 0 NORMAL
        @parameter mode 1 WAKEUP
        @parameter mode 2 POWERSAVE
        @parameter mode 3 SLEEP

        """
        if mode not in [0,1,2,3]:
            print('Invalid mode',mode)
        else:
            #print('setmode',mode)
            if self.pythontype == 0:
                if mode == 0:
                    self.m0.low()
                    self.m1.low()
                elif mode == 1:
                    self.m0.high()
                    self.m1.low()
                elif mode == 2:
                    self.m0.low()
                    self.m1.high()
                elif mode == 3:
                    self.m0.high()
                    self.m1.high()

            else:
                if mode == 0:
                    self.m0.value = 0 
                    self.m1.value = 0
                elif mode == 1:
                    self.m0.value = 1
                    self.m1.value = 0
                elif mode == 2:
                    self.m0.value = 0
                    self.m1.value = 1
                elif mode == 3:
                    self.m0.value = 1
                    self.m1.value = 1
            self.mode = mode
            #time.sleep_ms(2)
            time.sleep(0.002)

    def getMode(self):
        return self.mode

    def reset(self):
        self.setMode(3)
        #before = self.aux.value()
        self.serial.write( b'\XC4\XC4\XC4')
        #start = time.ticks_ms()
        #time.sleep_ms(5)
        time.sleep(0.005)
        #after = self.aux.value()
        if self.pythontype == 0:
            while self.aux.value() == 0:
                pass
        else:
            while self.aux.value == 0:
                pass
        #elapsed = time.ticks_ms() - start
        if self.debug:
            #print('AUX b %d a %d'%(before,after))
            #print('Reset %dms'%(elapsed))
            pass
        
    def serClear(self):
        if self.pythontype == 0:
            while self.serial.any():
                self.serial.read()
        else:
            while self.serial.in_waiting > 0:
                self.serial.read()


    def getModule(self):
        """
        Print the module information for this device
        """
        self.setMode(3)
        self.serClear()
        self.serial.write( b'\xc3\xc3\xc3')
        #time.sleep_ms(10)
        time.sleep(0.010)
        d = self.serial.read()
        # print(d)
        # wait for AUX to go down
        if self.pythontype == 0:
            while self.aux.value() == 0:
                pass
        else:
            while self.aux.value == 0:
                pass
        data = bytes(d)
        if len(data) != 4:
            print("getModule data length wrong")
        else:
            if data[0] != 0xC3:
                print('getModule header wrong')
            else:
                if data[1] == 0x32:
                    print('433Mhz')
                elif data[1] == 0x45:
                    print('900Mhz')
                else:
                    print('???Mhz')
            print('Version %2X' % data[2])
            print('max %d dBm'% data[3])

    def getData(self):
        """
        Get incoming data (if any).
        """ 
        # self.setMode(0) # should already be mode 0/1
        if self.pythontype == 0:
            if self.serial.any():
                return self.serial.read()
            else:
                return None
        else:
            #print('cp',self.serial.in_waiting)
            if self.serial.in_waiting > 0:
                d = self.serial.read(self.serial.in_waiting)
                return d
            else:
                return None
            
    def getConfig(self):
        """
        Make a local copy of this devices configuration
        If there is already a local copy it will get overwritten
        """
        self.haveconfig = False
        self.setMode(3)
        self.serClear()
        before = -1
        after = -1
        if self.pythontype == 0:
            before = self.aux.value()
        else:
            before = self.aux.value
            
        self.serial.write( b'\xc1\xc1\xc1')
        #start = time.ticks_ms()
        #time.sleep_ms(5)  # why do I need this?
        time.sleep(0.005)
        if self.pythontype == 0:
            #after = self.aux.value()
            while self.aux.value() == 0:
                pass
        else:
            #after = self.aux.value
            while self.aux.value == 0:
                pass
        # wait for AUX to go down
       # while self.aux.value() == 0:
        #    pass
        #elapsed = time.ticks_ms() - start
        d = self.serial.read()
        if self.debug:
            #print('AUX b %d a %d'%(before,after))
            #print('getConfig',d,type(d),' Elapsed time',elapsed)
            pass
        if type(d) is bytes and len(d) == 6 and d[0] == 0xc0:
            # d is a bytes which is non-mutable, change to bytearray
            # needed for following setXXX functions           
            self.config = bytearray(d) 
            self.haveconfig = True
        else:
            print('getConfig data bad')
            return

    def printConfig(self):
        if not self.haveconfig:
            print('No local config available')
            return
        print("Configuration")
        if self.debug:
            print('%02X %02X %02X %02X %02X %02X'%(self.config[0],self.config[1],self.config[2],self.config[3],self.config[4],self.config[5]))
        print('ADDH %d'%self.config[1])
        print('ADDL %d'%self.config[2])
        parity = (self.config[3] & 0xc0) >> 6
        print(self.paritytypes[parity])
        baud = (self.config[3] & 0x38) >> 3
        print(self.baudtypes[baud])
        airRate = self.config[3] & 0x7
        print(self.ratetypes[airRate])
        print('Channel',self.config[4] & 0x1f)
        if (self.config[5] & 0x80) == 0:
            print('Transparent mode')
        else:
            print('Fixed mode')
        if (self.config[5] & 0x40) == 0:
            print('Open mode')
        else:
            print('Pullup mode')
        wakeup = (self.config[5] & 0x38) >> 3
        print(self.waketypes[wakeup])
        if (self.config[5] & 0x4) == 0:
            print('FEC off')
        else:
            print('FEC on')
        power = self.config[5] & 0x3
        print(self.powertypes[power])

    def sendTransparentMessage(self,msg):
        """
        Send a message from this device
        @parameter msg Must be an str or a bytes object, no greater than 58 bytes
        """
        if type(msg) is bytes or type(msg) is str:
            if len(msg) < 59:
                self.setMode(0)
                if self.debug:
                    print('Sending',msg,'type',type(msg))
                if type(msg) is bytes:
                    self.serial.write(msg) #,len(msg))
                else:
                    self.serial.write(bytes(bytearray(msg))) #,len(msg))
                if self.pythontype == 0:
                    while self.aux.value() == 0:
                        pass
                else:
                    while self.aux.value == 0:
                        pass
            else:
                print('Maximum message length 58 bytes')
        else:
            print('Message must bytes or str')

    def sendFixedMessage(self,addh,addl,channel,msg):
        """
        Send a message from this device
        @parameter msg Must be an str or a bytes object, no greater than 58 bytes
        """
        if type(msg) is bytes or type(msg) is str:
            if len(msg) < 59:
                self.setMode(0)
                if self.debug:
                    print('Sending to %d:%d channel %d'%(addh,addl,channel),msg)
                ba = ''
                if type(msg) is str:
                    ba = bytes(bytearray((addh,addl,channel))+bytearray(msg))
                else:
                    ba = bytes(bytearray((addh,addl,channel)))+msg
                self.serial.write(ba) #,len(ba))
                if self.pythontype == 0:
                    while self.aux.value() == 0:
                        pass
                else:
                    while self.aux.value == 0:
                        pass
            else:
                print('Maximum message length 58 bytes')
        else:
            print('Message must bytes or str')

    def getlocalconfig(self):
        while not self.haveconfig:
            savedebug = self.debug
            self.debug = False
            self.getConfig()
            self.debug = savedebug        

    def setAddress(self,addh,addl):
        """
        Set the ADDH and ADDL fields in the local copy of configuration
        @parameter addh int
        @parameter addl int
        """
        self.getlocalconfig()
        self.config[1] = addh
        self.config[2] = addl

    def setParity(self,par):
        """
        Set the UART parity field in the local copy of configuration
        @parameter par A (See datasheet section 7.5)
        """
        self.getlocalconfig()
        self.config[3] = (self.config[3] & 0x3f) | (par<<6)

    def setUARTbaudrate(self,baud):
        """
        Set the UART baudrate field in the local copy of configuration
        @parameter baud (See datasheet section 7.5)
        """
        if type(baud) == int and baud >= 0 and baud <=7:
            self.getlocalconfig()
            self.config[3] = (self.config[3] & 0xc7) | (baud<<3)
        else:
            print('baud must be integer 0 to 7')            

    def setAirRate(self,ar):
        """
        Set the Air Data rate field in the local copy of configuration
        @parameter ar (See datasheet section 7.5)
        """
        self.getlocalconfig()
        self.config[3] = (self.config[3] & 0xf8) | ar

    def setChannel(self,ch):
        """
        Set the channel number in the local copy of configuration
        @parameter baud (See datasheet section 7.5)
        """
        self.getlocalconfig()
        self.config[4] = (self.config[4] & 0xe0) | ch

    def setFixedTransparent(self,onoff):
        """
        Set the Fixed/Transparent bit in the local copy of configuration
        @parameter onoff True or False (See datasheet section 7.5)
        """
        self.getlocalconfig()
        if onoff:
            self.config[5] = self.config[5] | 0x80 # bit 7 on
        else:
            self.config[5] = self.config[5] & 0x7f # bit 7 off
       
    def setPullup(self,onoff):
        """
        Set the Pullup/Open bit in the local copy of configuration
        @parameter onoff True or False (See datasheet section 7.5)
        """
        self.getlocalconfig()
        if onoff:
            self.config[5] = self.config[5] | 0x40 # bit 6 on
        else:
            self.config[5] = self.config[5] & 0xBF # bit 6 off

    def setWakeup(self,wu):
        """
        Set the Wakeup in the local copy of configuration
        @parameter wu (See datasheet section 7.5)
        """
        self.getlocalconfig()
        self.config[5] = (self.config[5] & 0xC7) | (wu << 3)

    def setFEC(self,onoff):
        """
        Set the FEC bit in the local copy of configuration
        @parameter onoff True or False (See datasheet section 7.5)
        """
        self.getlocalconfig()
        if onoff:
            self.config[5] = self.config[5] | 0x04 # bit 2 on
        else:
            self.config[5] = self.config[5] & 0xFB # bit 2 off

    def setPower(self,pw):
        """
        Set the Power field in the local copy of configuration
        @parameter pw (See datasheet section 7.5)
        """
        self.getlocalconfig()
        self.config[5] = (self.config[5] & 0xFC) | pw

    def setConfig(self,save):
        """
        Save the local copy of configuration to the device
        @parameter save. If True the configuration is saved when powered down, else is lost when 
                    powered down
        """
        if self.haveconfig:
            if self.debug:
                print('setConfig', save)
            self.setMode(3)
            if save:
                self.config[0] = 0xc0
            else:
                self.config[0] = 0xc2
            #before = self.aux.value()
            #start = time.ticks_ms()
            self.serial.write(self.config) #,6)
            #time.sleep_ms(2)
            time.sleep(0.002)
            if self.pythontype == 0:
                #after = self.aux.value()
                while self.aux.value() == 0:
                    pass
            else:
                while self.aux.value == 0:
                    pass
            if self.debug:
                #print('AUX b %d a %d'%(before,after))
                #print('setConfig %dms'%(time.ticks_ms() - start))
                pass
            #time.sleep(1)
        else:
            print('No config to save')