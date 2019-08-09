
import pigpio
import time
import threading

class us_distance(threading.Thread):

    def __init__(self,pi=None,GPIO_TRIGGER=23,GPIO_ECHO=24):

        threading.Thread.__init__(self)
        self.pi = pi if pi is not None else pigpio.pi()

        self.GPIO_ECHO = GPIO_ECHO
        self.GPIO_TRIGGER = GPIO_TRIGGER
        self.pi.set_mode(GPIO_TRIGGER,pigpio.OUTPUT)
        self.pi.set_mode(GPIO_ECHO, pigpio.INPUT)
        self.dist = 0  ## lastgood

        self.needToStop = False

    def distance(self):
        # set Trigger to HIGH
        dist = 0
        self.pi.gpio_trigger(self.GPIO_TRIGGER,10,1)  # set Trigger after 0.01ms to LOW

        absstart = StopTime = StartTime = time.time()

        '''
        if pi.wait_for_edge(self.GPIO_ECHO,pigpio.RISING_EDGE,2.0):
            StartTime = time.time()
        else:
            return 1000000 # timeout
    
        if pi.wait_for_edge(self.GPIO_ECHO,pigpio.FALLING_EDGE,2.0):
            StopTime  = time.time()
        else:
            return 1000000 # timeout
        '''


        while pi.read(self.GPIO_ECHO) == 0:
            StartTime = time.time()
            if StartTime > absstart + 1: return 2000000

        # save time of arrival
        absstart = StartTime
        while pi.read(self.GPIO_ECHO) == 1:
            StopTime = time.time()
            if StopTime > absstart + 1: return 1000000

        dist = ((StopTime - StartTime) * 34300) / 2

        return dist

    def run(self):
        self.needToStop = False
        while not self.needToStop:
            d = self.avgdistance()
            #print "Avg %.1f" % d
            time.sleep(0.5)
    def stop(self):
        self.needToStop = True

    def avgdistance(self):


        good_attempts = 3
        good__median_ndx = 1
        good_values = [0,0,0]
        total_attempts = 15
        sum = 0
        attempts = good_attempts
        while True:
            dist = self.distance()
            if total_attempts<=0:
                self.dist = 0
                return 1000000 ## error
            total_attempts-=1
            if dist>1000 or dist <1:
                time.sleep(0.2)
                continue
            sum+=dist
            attempts-=1
            good_values[attempts]=dist
            if attempts<=0:
#                self.dist = sum/good_attempts
                self.dist = good_values[good__median_ndx]   ## median
                return self.dist

            time.sleep(0.01)

if __name__ == '__main__':

    pi = pigpio.pi()  # Connect to Pi.
    if not pi.connected:
        pi = pigpio.pi("192.168.3.74")  # Connect to Pi.


    if not pi.connected:
        print "Unable to connect, exiting"
        exit()
    dm = us_distance(pi,23,24)
    dm.start()

    try:

        while True:

            print "Dist %.1f" % dm.dist
            time.sleep(1)
            #print ("Measured Distance = %.1f cm" % dm.distance())
            #print ("Avg Measured Distance = %.1f cm" % dm.avgdistance())
            #time.sleep(0.5)
            # Reset by pressing CTRL + C


    except KeyboardInterrupt:
        print("Measurement stopped by User")


    dm.stop()
    print("Requested stop")
    dm.join()
    print("Stopped")
    pi.stop()

