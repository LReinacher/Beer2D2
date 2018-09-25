import pigpio
import time

pi = pigpio.pi() 
pi.set_mode(13, pigpio.OUTPUT) # GPIO 17 as output
pi.set_PWM_dutycycle(13, 0) # PWM off
pi.set_mode(18, pigpio.OUTPUT) # GPIO 17 as output
pi.set_PWM_dutycycle(18, 0) # PWM off

#while True:
 #   print('1')
  #  pi.set_PWM_dutycycle(13, 255)
   # time.sleep(5)
    #print('2')
    #pi.set_PWM_dutycycle(13, 100)
    #time.sleep(5)