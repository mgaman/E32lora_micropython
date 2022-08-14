# E32lora
This is a work in progresss. The code works seamlessly for both micropython and circuitpython.  
For my development I have micropython on a Pico and circuitpython on a MakerPi.  
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
<b>E32lora(serial,aux,m0,m1)</b><p>
<ol>
<li>serial An UART object created by the caller</li>
<li>aux, m0, m1 GPIO pins. Integer for micropython, board.GPn for circuitpython. See the examples
in tests.py</li>
</ol>

## Methods
<b>setDebug(true-false)</b><p>
Turn internal debugging messages on/off.  
<b>setMode(n)</b><p>
Set the mode to Normal, Wakeup, PowerSave or Sleep.  
<b>getConfig()</b><p>
Get a local copy of this devices configuration data. Not needed if you do not intend to make changes.  
<b>printConfig()</b><p>
Print out a readable report of the local copy of configuration data.  
<b>setConfig(true-false)</b><p>
Write the local copy of the configuration back to the device. If *action* is *True* the data is retained upon powerdown, else *False* will not retain the data.  

The following functions all modify the local copy of configuration. To understand the values to write, read the datasheet, section 7.5.  

<b>setAddress(addh,addl)</b><p>
<b>SetParity(n)</b><p>
<b>setUARTbaudrate(n)</b><p>
<b>setAirRate(n)</b><p>
<b>setChannel(n)</b><p>
<b>setWakeup(n)</b><p>
<b>setPower(n)</b><p>

The following functions take a True/False argument to turn flags on or off.  
<b>setFixedTransparent(true-false)</b><p>
<b>setPullup(true-false)</b><p>
<b>setFEC(true-false)</b><p>

<b>sendTransparentMessage(msg)</b><p>
msg must be a *bytes* or *str* object. The maximum length of msg is 58 bytes, according to the manual. Use this when in *Transparent* mode.  
<b>sendFixedMessage(addrh,addrl,channel,msg)</b><p>
<ol>
<li>addrh - int target address high</li>  
<li>addrl - int  target address low  </li> 
<li>channel - int  target channel  </li> 
<li>msg - message payload, a <i>bytes</i> or <i>string</i> object</li>
</ol>
Use this when in <i>Fixed</i> mode.<p>
<b>getData()</b><p>
Returns <i>None</i> if no data available, else a <i>bytearray</i>.

# Testing
I aimed to keep my workspace simple so adopted the following strategy.  
The same files are downloaded to all Picos used in testing.
## E32lora.py
This is the Class that controls the device
## tests.py
Contains a collection of functions to implement various transmit/receive scenarios
## main.py
Uses a pin to set the device into transmit or receive mode. If the pin is left open the transmit function is executed. If shorted to ground the receive function is executed.
# Anomalies
<ol>
<li>According to the datasheet when broadcasting one must use an address of 0x0000 or 0xFFFF. In practice I only got 0xFFFF to work.</li>
<li>According to the datasheet AUX goes LOW immediately upon receiving a command. I measured, in practice, that it goes down
after a delay of a few millisecs. See the code for actual values.</li>
</ol>

# Outstanding Issues
I have yet to conduct tests of all the various settings that can be changed e.g. power level, FEC.
# Releases
## 0.1
Initial working version
## 0.2
Replaced sendMessage by sendTransparentMessage and sendFixedMessage. Not 100% necessary but makes life simpler for the user.  
Changed the argument of setAddr() from a tuple to 2 integers. This was done to make a consistent interface to sendFixedMessage.  
## 0.3
Tweaked the use of AUX for signalling end of operation
## 0.4
Added support for circuitpython
