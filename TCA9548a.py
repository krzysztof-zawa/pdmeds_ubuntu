import time
import lgpio
import BMP180v3
#ustawienie RESet

# BMP085 default address.
BMP180_I2CADDR           = 0x77


# Operating Modes
BMP180_ULTRALOWPOWER     = 0
BMP180_STANDARD          = 1
BMP180_HIGHRES           = 2
BMP180_ULTRAHIGHRES      = 3

# BMP085 Registers
BMP180_CAL_AC1           = 0xaa  # R   Calibration data (16 bits)
BMP180_CAL_AC2           = 0xac  # R   Calibration data (16 bits)
BMP180_CAL_AC3           = 0xae  # R   Calibration data (16 bits)
BMP180_CAL_AC4           = 0xb0  # R   Calibration data (16 bits)
BMP180_CAL_AC5           = 0xB2  # R   Calibration data (16 bits)
BMP180_CAL_AC6           = 0xB4  # R   Calibration data (16 bits)
BMP180_CAL_B1            = 0xB6  # R   Calibration data (16 bits)
BMP180_CAL_B2            = 0xB8  # R   Calibration data (16 bits)
BMP180_CAL_MB            = 0xBA  # R   Calibration data (16 bits)
BMP180_CAL_MC            = 0xBC  # R   Calibration data (16 bits)
BMP180_CAL_MD            = 0xBE  # R   Calibration data (16 bits)
BMP180_CONTROL           = 0xF4
BMP180_TEMPDATA          = 0xF6
BMP180_PRESSUREDATA      = 0xF6

# Commands
BMP180_READTEMPCMD       = 0x2E
BMP180_READPRESSURECMD   = 0x34



reset_pin = 4
a0_pin = 17
a1_pin = 27
a2_pin = 22
mux_address = 0x70

gpio = lgpio.gpiochip_open(0)



try:
    lgpio.gpio_claim_output(gpio, reset_pin, 1)
    lgpio.gpio_claim_output(gpio, a0_pin, 0)
    lgpio.gpio_claim_output(gpio, a1_pin, 0)
    lgpio.gpio_claim_output(gpio, a2_pin, 0)
except KeyboardInterrupt:
    lgpio.gpiochip_close(gpio)
    lgpio.gpiochip_close(gpio)
    lgpio.gpiochip_close(gpio)
    lgpio.gpiochip_close(gpio)



#porba odblokowania kanau 1

i2c = lgpio.i2c_open(1, mux_address)
lgpio.i2c_write_byte_data(i2c, mux_address, 0b00000001)

#lgpio.i2c_write_byte_data(i2c, BMP180_CONTROL, BMP180_READTEMPCMD)
#time.sleep(0.01)  # Wait 5ms
#raw = self._device.readU16BE(BMP085_TEMPDATA)
#(x, raw_byte) = lgpio.i2c_read_i2c_block_data(i2c, BMP180_TEMPDATA, 2)
#raw = int.from_bytes(raw_byte, 'big')
#print(raw)
bmp1 = BMP180v3.BMP180()
bmp1.read_temperature()
bmp1.read_pressure()
bmp1.read_altitude()
bmp1.close_i2c()

lgpio.i2c_write_byte_data(i2c, mux_address, 0b00000010)
bmp2 = BMP180v3.BMP180()
bmp2.read_temperature()
bmp2.read_pressure()
bmp2.read_altitude()
bmp2.close_i2c()

#lgpio.i2c_write_byte_data(i2c, mux_address, 0b00000000)


