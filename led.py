from machine import Pin
class Led:
    def __init__(self,ledpin):
        self.ledpin = Pin(ledpin,Pin.OUT)
        self.ledstate = False
        self.ledpin.value(0)

    def ledOn(self):
        self.ledpin.value(1)
        self.ledstate = True

    def ledOff(self):
        self.ledpin.value(0)
        self.ledstate = False

    def ledToggle(self):
        if self.ledstate:
            self.ledOff()
        else:
            self.ledOn()
