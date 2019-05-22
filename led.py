
import RPi.GPIO as GPIO
import time
from time import sleep

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
led = 25
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(led, GPIO.OUT)


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed *34000) / 2
 
    return distance 

p = GPIO.PWM(led,50)
p.start(0);
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if distance() <= 10:
               for dc in range(50,101,5):
                   p.ChangeDutyCycle(dc)
                   sleep(0.1)
            elif 20 <= distance() > 10:
               for dc in range(11,-1,-5):
                   p.ChangeDutyCycle(dc)
                   sleep(0.1)
            else:
               for dc in range(0,-1,-5):
                   p.ChangeDutyCycle(dc)
                   sleep(0.1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        p.stop()
        GPIO.cleanup()

