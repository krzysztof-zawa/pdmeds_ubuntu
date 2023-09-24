import time
import BMP180v3
import TCA9548a_v2

if __name__ == "__main__":
    tca = TCA9548a_v2.TCA9548a(address= TCA9548a_v2.ADDRESS_2)
    tca.select_channel(TCA9548a_v2.CHANNEL_0)
    bmp1 = BMP180v3.BMP180()
    bmp1.read_temperature()
    bmp1.read_pressure()
    tca.lock_channel()

    tca.select_channel(TCA9548a_v2.CHANNEL_1)
    bmp2 = BMP180v3.BMP180()
    bmp2.read_temperature()
    bmp2.read_pressure()
    tca.lock_channel()


    tca.select_channel(TCA9548a_v2.CHANNEL_0)   
    bmp1.read_temperature()
    bmp1.read_pressure()
    tca.lock_channel()
    tca.select_channel(TCA9548a_v2.CHANNEL_1)   
    bmp2.read_temperature()
    bmp2.read_pressure()
    tca.lock_channel()