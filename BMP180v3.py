import time
import lgpio

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

class BMP180():
    def __init__(self, mode = BMP180_STANDARD, address = BMP180_I2CADDR):
        #check if mode is valid
        if mode not in [BMP180_ULTRALOWPOWER, BMP180_STANDARD, BMP180_HIGHRES, BMP180_ULTRAHIGHRES]:
            raise ValueError('Unexpected mode value {0}.  Set mode to one of BMP085_ULTRALOWPOWER, BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES'.format(mode))
        self._mode = mode
        #create i2c device
        self.h = lgpio.i2c_open(1, BMP180_I2CADDR)
        self.load_calibration()

    def load_calibration(self):
        (x, self.cal_AC1_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_CAL_AC1, 2)   # INT16
        (x, self.cal_AC2_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_CAL_AC2, 2)   # INT16
        (x, self.cal_AC3_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_CAL_AC3, 2)   # INT16
        (x, self.cal_AC4_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_CAL_AC4, 2)   # UINT16
        (x, self.cal_AC5_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_CAL_AC5, 2)   # UINT16
        (x, self.cal_AC6_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_CAL_AC6, 2)   # UINT16
        (x, self.cal_B1_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_CAL_B1, 2)     # INT16
        (x, self.cal_B2_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_CAL_B2, 2)    # INT16
        (x, self.cal_MB_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_CAL_MB, 2)     # INT16
        (x, self.cal_MC_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_CAL_MC, 2)     # INT16
        (x, self.cal_MD_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_CAL_MD, 2)  

        
        self.cal_AC1 = int.from_bytes(self.cal_AC1_byte, 'big')
        self.cal_AC2 = int.from_bytes(self.cal_AC2_byte, 'big')
        self.cal_AC3 = int.from_bytes(self.cal_AC3_byte, 'big')
        self.cal_AC4 = int.from_bytes(self.cal_AC4_byte, 'big')
        self.cal_AC5 = int.from_bytes(self.cal_AC5_byte, 'big')
        self.cal_AC6 = int.from_bytes(self.cal_AC6_byte, 'big')
        self.cal_B1 = int.from_bytes(self.cal_B1_byte, 'big')
        self.cal_B2 = int.from_bytes(self.cal_B2_byte, 'big')
        self.cal_MB = int.from_bytes(self.cal_MB_byte, 'big')
        self.cal_MC = int.from_bytes(self.cal_MC_byte, 'big')
        self.cal_MD = int.from_bytes(self.cal_MD_byte, 'big')
       
        self.cal_AC1 = self.negative_number(self.cal_AC1)
        self.cal_AC2 = self.negative_number(self.cal_AC2)
        self.cal_AC3 = self.negative_number(self.cal_AC3)
       
        self.cal_B1 = self.negative_number(self.cal_B1)
        self.cal_B2 = self.negative_number(self.cal_B2)
        self.cal_MB = self.negative_number(self.cal_MB)
        self.cal_MC = self.negative_number(self.cal_MC)
        self.cal_MD = self.negative_number(self.cal_MD)

        


       

    def _load_datasheet_calibration(self):
        # Set calibration from values in the datasheet example.  Useful for debugging the
        # temp and pressure calculation accuracy.
        self.cal_AC1 = 408
        self.cal_AC2 = -72
        self.cal_AC3 = -14383
        self.cal_AC4 = 32741
        self.cal_AC5 = 32757
        self.cal_AC6 = 23153
        self.cal_B1 = 6190
        self.cal_B2 = 4
        self.cal_MB = -32767
        self.cal_MC = -8711
        self.cal_MD = 2868

    def read_raw_temp(self):
        """Reads the raw (uncompensated) temperature from the sensor."""
        #self._device.write8(BMP085_CONTROL, BMP085_READTEMPCMD)
        lgpio.i2c_write_byte_data(self.h, BMP180_CONTROL, BMP180_READTEMPCMD)
        time.sleep(0.01)  # Wait 5ms
        #raw = self._device.readU16BE(BMP085_TEMPDATA)
        (x, raw_byte) = lgpio.i2c_read_i2c_block_data(self.h, BMP180_TEMPDATA, 2)
        raw = int.from_bytes(raw_byte, 'big')
        return raw

    def read_raw_pressure(self):
        """Reads the raw (uncompensated) pressure level from the sensor."""
        #self._device.write8(BMP085_CONTROL, BMP085_READPRESSURECMD + (self._mode << 6))
        lgpio.i2c_write_byte_data(self.h, BMP180_CONTROL, BMP180_READPRESSURECMD + (self._mode << 6))
        if self._mode == BMP180_ULTRALOWPOWER:
            time.sleep(0.0045)
        elif self._mode == BMP180_HIGHRES:
            time.sleep(0.014)
        elif self._mode == BMP180_ULTRAHIGHRES:
            time.sleep(0.026)
        else:
            time.sleep(0.008)
        msb = lgpio.i2c_read_byte_data(self.h, BMP180_PRESSUREDATA)
        lsb = lgpio.i2c_read_byte_data(self.h, BMP180_PRESSUREDATA+1)
        xlsb = lgpio.i2c_read_byte_data(self.h, BMP180_PRESSUREDATA+2)
        raw = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self._mode)
        return raw

    def read_temperature(self):
        """Gets the compensated temperature in degrees celsius."""
        UT = self.read_raw_temp()
        # Datasheet value for debugging:
        #UT = 27898
        # Calculations below are taken straight from section 3.5 of the datasheet.
        X1 = ((UT - self.cal_AC6) * self.cal_AC5)/pow(2,15)
        X2 = (self.cal_MC * pow(2,11)) / (X1 + self.cal_MD)
        B5 = X1 + X2
        temp = ((B5 + 8)/pow(2,4)) / 10.0
        print('Calibrated temperature {0} C'.format(temp))
        return temp

    def read_pressure(self):
        """Gets the compensated pressure in Pascals."""
        UT = self.read_raw_temp()
        UP = self.read_raw_pressure()
        # Datasheet values for debugging:
        #UT = 27898
        #UP = 23843
        # Calculations below are taken straight from section 3.5 of the datasheet.
        # Calculate true temperature coefficient B5.
        X1 = ((UT - self.cal_AC6) * self.cal_AC5) >> 15
        X2 = (self.cal_MC << 11) // (X1 + self.cal_MD)
        B5 = X1 + X2
        # Pressure Calculations
        B6 = B5 - 4000
        X1 = (self.cal_B2 * (B6 * B6) >> 12) >> 11
        X2 = (self.cal_AC2 * B6) >> 11
        X3 = X1 + X2
        B3 = (((self.cal_AC1 * 4 + X3) << self._mode) + 2) // 4
        X1 = (self.cal_AC3 * B6) >> 13
        X2 = (self.cal_B1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self.cal_AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> self._mode)
        if B7 < 0x80000000:
            p = (B7 * 2) // B4
        else:
            p = (B7 // B4) * 2
        X1 = (p >> 8) * (p >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * p) >> 16
        p = p + ((X1 + X2 + 3791) >> 4)
        print('Pressure {0} Pa'.format(p))
        return p

    def read_altitude(self, sealevel_pa=101325.0):
        """Calculates the altitude in meters."""
        # Calculation taken straight from section 3.6 of the datasheet.
        pressure = float(self.read_pressure())
        altitude = 44330.0 * (1.0 - pow(pressure / sealevel_pa, (1.0/5.255)))
        print('Altitude {0} m'.format(altitude))
        return altitude

    def read_sealevel_pressure(self, altitude_m=0.0):
        """Calculates the pressure at sealevel when given a known altitude in
        meters. Returns a value in Pascals."""
        pressure = float(self.read_pressure())
        p0 = pressure / pow(1.0 - altitude_m/44330.0, 5.255)
        print('Sealevel pressure {0} Pa'.format(p0))
        return p0
    def close_i2c(self):
        lgpio.i2c_close(self.h)

    def negative_number(self, num):
        if num > 32767:
            num = num - 65535
        return num 
        

    def load_numbers(self):
        self.cal_AC1 = 8377
        self.cal_AC2 = -1127
        self.cal_AC3 = -14498
        self.cal_AC4 = 34267
        self.cal_AC5 = 25242
        self.cal_AC6 = 20124
        self.cal_B1 = 6515
        self.cal_B2 = 42
        self.cal_MB = -32767
        self.cal_MC = -11785
        self.cal_MD = 2672

if __name__ == "__main__":
    bmp = BMP180()
    bmp.read_temperature()
    bmp.read_pressure()
    bmp.read_altitude()
    bmp.close_i2c()