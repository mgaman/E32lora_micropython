# E32lora
This is a work in progresss. So far there is a version written for micropython and tested on the RaspberryPi Pico.  
The only device I have is an E32-900T20D. I assume the code will work for all devices in the family but interpretations of configuration data (e.g. power level) may differ.  
I am assuming all pins are connected.  
Please try this out on as many boards/devices as you can and feed the results back to me.
```
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
```
# API
## Constructor
E32lora(serial,aux,m0,m1)
### serial
An UART object created by the caller
### aux, m0, m1
GPIO numbers of the relevant pins.
## setDebug(true-false)
Turn internal debugging messages on/off
## setMode(n)
Set the mode to Normal, Wakeup, PowerSave or Sleep.
## getConfig()
Get a local copy of this devices configuration data. Not needed if you do not intend to make changes
## printConfig()
Print out a readable report of the local copy of configuration data
## setConfig(true-false)
Write the local copy of the configuration back to the device. If *action* is *True* the data is retained upon powerdown, else *False* will not retain the data.  
The following functions all modify the local copy of configuration. To understand the values to write, read the datasheet, section 7.5.  

## SetParity(n)
## setUARTbaudrate(n)
## setAirRate(n)
## setChannel(n)
## setWakeup(n)
## setPower(n)

The following functions take a True/False argument to turn flags on or off.
## setFixedTransparent(true-false)
## setPullup(true-false)
## setFEC(true-false)

## sendMessage(msg)
msg must be a *bytes* or *str* object. The maximum length of msg is 58 bytes, according to the manual.
## getData()
Returns *None* if no data available, else a *bytearray*.
# Testing
I aimed to keep my workspace simple so adopted the following strategy.  
## E32lora.py
This is the Class that controls the device
## mytest.py
Contains a collection of functions to implement various transmit/receive scenarios
## main.py
Uses pin 12 to set the device into transmit or receive mode. If Pin 12 is left open the transmit function is executed. If shorted to
ground the receive function is executed.
# Anomalies
According to the datasheet when broadcasting to may use an address of 0x0000 or 0xFFFF. In practice I only got 0xFFFF to work.
# Outstanding Issues
One should be able be able to monitor the AUX pin transitioning from LOW to HIGH to judge when an action has completed. I have yet to get this to work in practice so have used timed delays instead. Unprofessional but it works.  