import lgpio
import time


servo = 18
pulse_width = 1000
servo_freq = 50
pulse_offset = 0
pulse_cycles = 0

print(list)
h= lgpio.gpiochip_open(0)

try:
    while True:
        lgpio.tx_servo(h, servo, 500, servo_freq, pulse_offset, 0)
        print("MOVE 0 DEG")
        time.sleep(5)
        
        
        lgpio.tx_servo(h, servo, 1000, servo_freq, pulse_offset, 30)
        print("MOVE 45 DEG")
        time.sleep(5)
        

        lgpio.tx_servo(h, servo, 1500, servo_freq, pulse_offset, 30)
        print("MOVE 90 DEG")
        time.sleep(5)

        lgpio.tx_servo(h, servo, 2000, servo_freq, pulse_offset, 30)
        print("MOVE 135 DEG")
        time.sleep(5)

        lgpio.tx_servo(h, servo, 2500, servo_freq, pulse_offset, 30)
        print("MOVE 180 DEG")
        time.sleep(5)
        
            

except KeyboardInterrupt:
    lgpio.gpiochip_close(h)