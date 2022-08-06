# E32lora
This is a work in progresss. So far there is a version written for micropython and tested on the RaspberryPi Pico.  
The only device I have is an E32-900T20D. I assume the code will work for all devices in the family but interpretations of configuration data (e.g. power level) may differ.  
I am assuming all pins are connected.  
Please try this out on as many boards/devices as you can and feed the results back to me.
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
## setConfig(action)
Write the local copy of the configuration back to the device. If *action* is *True* the data is retained upon powerdown, else *False* will not retain the data.  
The following functions all modify the local copy of configuration. To understand the values to write, read the datasheet, section 7.5.  

## SetParity(n)
## setUARTbaudrate(n)
## setAirRate(n)
## setChannel(n)
## setWakeup(n)
## setPower(n)

The following finctions take a True/False argument to turn flags on or off.
## setFixedTransparent(true-false)
## setPullup(true-false)
## setFEC(true-false)

# Testing
I aimed to keep my workspace simple so adopted the following strategy.  
## E32lora.py
This is the Class that controls the device
## mytest.py
Contains a collection of functions to implement various transmit/receive scenarios
## main.py
Uses pin 12 to set the device into transmit or receive mode. If Pin 12 is left open the transmit function is executed. If shorted to
ground the receive function is executed.

