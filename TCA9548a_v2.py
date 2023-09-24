import time
import lgpio


#POSSIBLE ADDRESSES OF MUX
ADDRESS_1 = 0x70
ADDRESS_2 = 0X71
ADDRESS_3 = 0x72
ADDRESS_4 = 0X73
ADDRESS_5 = 0x74
ADDRESS_6 = 0X75
ADDRESS_7 = 0x76
ADDRESS_8 = 0X77

#GPIO PINS
RESET = 4
A0 = 17
A1 = 27
A2 = 22

#channels
CHANNEL_LOCK = 0b00000000
CHANNEL_0 = 0b00000001
CHANNEL_1 = 0b00000010
CHANNEL_2 = 0b00000100
CHANNEL_3 = 0b00001000
CHANNEL_4 = 0b00010000
CHANNEL_5 = 0b00100000
CHANNEL_6 = 0b01000000
CHANNEL_7 = 0b10000000

class TCA9548a():
    def __init__(self, address = ADDRESS_1):
        if address not in [ ADDRESS_1, 
                            ADDRESS_2,
                            ADDRESS_3,
                            ADDRESS_4,
                            ADDRESS_5,
                            ADDRESS_6,
                            ADDRESS_7,
                            ADDRESS_8]:
            raise ValueError('Unexpected address value {0}.'.format(address))
        self.address = address
        self.gpio = lgpio. gpiochip_open(0)
        self.i2c = lgpio.i2c_open(1, self.address)
        self.init_gpio()


    def init_gpio(self):
        #Pull up reser pin
        lgpio.gpio_claim_output(self.gpio, RESET, 1)
        
        if self.address == 0x70:
            lgpio.gpio_claim_output(self.gpio, A0, 0)
            lgpio.gpio_claim_output(self.gpio, A1, 0)
            lgpio.gpio_claim_output(self.gpio, A2, 0)   
        elif self.address == 0x71:
            lgpio.gpio_claim_output(self.gpio, A0, 1)
            lgpio.gpio_claim_output(self.gpio, A1, 0)
            lgpio.gpio_claim_output(self.gpio, A2, 0)  
        elif self.address == 0x72:
            lgpio.gpio_claim_output(self.gpio, A0, 0)
            lgpio.gpio_claim_output(self.gpio, A1, 1)
            lgpio.gpio_claim_output(self.gpio, A2, 0)
        elif self.address == 0x73:
            lgpio.gpio_claim_output(self.gpio, A0, 1)
            lgpio.gpio_claim_output(self.gpio, A1, 1)
            lgpio.gpio_claim_output(self.gpio, A2, 0)
        elif self.address == 0x74:
            lgpio.gpio_claim_output(self.gpio, A0, 0)
            lgpio.gpio_claim_output(self.gpio, A1, 0)
            lgpio.gpio_claim_output(self.gpio, A2, 1)
        elif self.address == 0x75:
            lgpio.gpio_claim_output(self.gpio, A0, 1)
            lgpio.gpio_claim_output(self.gpio, A1, 0)
            lgpio.gpio_claim_output(self.gpio, A2, 1)
        elif self.address == 0x76:
            lgpio.gpio_claim_output(self.gpio, A0, 0)
            lgpio.gpio_claim_output(self.gpio, A1, 1)
            lgpio.gpio_claim_output(self.gpio, A2, 1)
        elif self.address == 0x77:
            lgpio.gpio_claim_output(self.gpio, A0, 1)
            lgpio.gpio_claim_output(self.gpio, A1, 1)
            lgpio.gpio_claim_output(self.gpio, A2, 1)
    def select_channel(self, channel):
        lgpio.i2c_write_byte_data(self.i2c, self.address, channel)
    def lock_channel(self):
        lgpio.i2c_write_byte_data(self.i2c, self.address, CHANNEL_LOCK)

if __name__ =="__main__":
    tca = TCA9548a()
    tca.select_channel(CHANNEL_0)
    time.sleep(20)
    tca.lock_channel()

