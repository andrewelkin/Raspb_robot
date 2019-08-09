try:
    import RPi.GPIO as GPIO
except:
    import gpiozero as GPIO
# to use Raspberry Pi board pin numbers

import time


common_pio = 13
sensors = [11,12]

names = ["Door","Motion"]


GPIO.setmode(GPIO.BOARD)

# set up the GPIO channels - one input and one output
for s in sensors:
    GPIO.setup(s, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(common_pio, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)


# input from pin 11
alerted = False
salerted = [False]*len(sensors)
delay = 0.1

while True:
    time.sleep(delay)
    common = GPIO.input(common_pio)
    if common ==0:
        if alerted:
            print "Idle state."

        alerted = False
        salerted = [False] * len(sensors)
        delay = 0.5
        continue

    if not alerted:
        print "Alert detected!"
        alerted = True
        delay = 0.1

    for i in range(len(sensors)):
        res = GPIO.input(sensors[i])
        if res ==0:
            if not salerted[i]:
                print "%s (%d)" %(names[i],sensors[i]), "Alerted"
                salerted[i] = True



