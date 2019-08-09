
import pigpio
import time
import morse

if __name__ == '__main__':

    pi = pigpio.pi()  # Connect to Pi.
    if not pi.connected:
        pi = pigpio.pi("192.168.3.74")  # Connect to Pi.



    while True:

        print "LED on"
        pi.write(19, 0)
        pi.write(26, 1)  ## right

        time.sleep(0.3)
        print "LED off"
        pi.write(19, 1)
        pi.write(26, 0)

        time.sleep(0.3)


