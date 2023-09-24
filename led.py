import time
import lgpio
import datetime
LED = 23

# open the gpio chip and set the LED pin as output
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, LED)

try:
    while True:
        
        for i in range(1,5):
            dt=0
            while dt<1:
                lgpio.gpio_write(h, LED,1)
                time.sleep(1/(i*5))
                lgpio.gpio_write(h, LED, 0)
                time.sleep(1/(i*5))
                dt = dt + 1/(i*5)
                
                
                
       
except KeyboardInterrupt:
    lgpio.gpio_write(h, LED, 0)
    lgpio.gpiochip_close(h)
