__author__ = 'Andy Elkin'
#!/usr/bin/python

import smbus
from ctypes import *
import os,sys

I2C_BUS_NO = 1


class I2CGeneral:
    def __init__(self,smsbusno=1):
        self.bus = smbus.SMBus(smsbusno)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
        self.addresses = set()

    def read_byte(self,addr):
        return self.bus.read_word_data(addr,0)

    def write_byte(self,addr, val) :
        self.bus.write_byte(addr,c_byte(val))

    def read_word_data(self,addr):
        return self.bus.read_word_data(addr,0)

    def write_word_data(self,addr, val) :
        self.bus.write_word_data(addr,c_int32(val))


    def DetectProbes(self):
        for i in range(128):
            try:
                self.bus.read_byte(i)
                self.addresses.add(i)
            except:
                pass

        return self.addresses


## LM75a temperature sensor. It gives temp with +-2C accuracy.  I suppose just shifting temp for a constant would give better resulnt
class LM75:
    def __init__(self,address,i2c=None,shift=0):
        self.addr = address
        self.shift = shift
        self.bus = I2CGeneral() if i2c is None else i2c

    def convertBitsToCelsiusFloat(self,byte1,byte0):
        retVal = 0.0
        if byte0 & 0x80 !=0:
            byte0 = (byte0 & 0x7f) - 128
        if byte1 & 0x80 ==0 :
            #  this is the case if the byte indicating the "0,5C" part was set  to 0 = no 1/2 degree was measured.
            retVal = byte0
        else:
            # very first bit of the  0,5C-indicator byte  was set to "1", so that this byte has a negative value --> a 1/2 degree was
            # // measured.
            retVal = byte0
            retVal = retVal + 0.5
        return retVal


    def getCurrentTemp(self):
        b = self.bus.read_word_data(self.addr)
        return  self.convertBitsToCelsiusFloat(b>>8,b & 0xFF) + self.shift


if __name__ == '__main__':

    DEVICE_ADDRESS = 0x48      #7 bit address (will be left shifted to add the read write bit)
    for g in sys.argv[1:]:
        if g.lower().startswith('/b:') or g.lower().startswith('-b:'):
            print "Using I2c bus %d" % I2C_BUS_NO
            I2C_BUS_NO = int (g[3:])

        if g.lower().startswith('/a:') or g.lower().startswith('-a:'):
            print "Using I2c probe address %X (%d)" % (DEVICE_ADDRESS,DEVICE_ADDRESS)
            DEVICE_ADDRESS = int (g[3:])

    i2c_bus = I2CGeneral(I2C_BUS_NO)

    for g in sys.argv[1:]:
        if g.lower().startswith('/d') or g.lower().startswith('-d'):
            probes = i2c_bus.DetectProbes()
            print "Detected %d probes on bus %d:" % (len(probes),I2C_BUS_NO),
            for j in list(probes):
                print "0x%X (%d) " % (j,j),
            print
            exit()

    print "Current temp is ",LM75(DEVICE_ADDRESS,i2c_bus,-2).getCurrentTemp()


'''
long write_quick(int addr) // Send only the read / write bit
long read_byte(int addr) //Read a single byte from a device, without specifying a device register.
long write_byte(int addr,char val) //Send a single byte to a device
long read_byte_data(int addr,char cmd) //Read Byte Data transaction.
long write_byte_data(int addr,char cmd,char val) //Write Byte Data transaction.
long read_word_data(int addr,char cmd) //Read Word Data transaction.
long write_word_data(int addr,char cmd,int val) //Write Word Data transaction.
long process_call(int addr,char cmd,int val) //Process Call transaction.
long[] read_block_data(int addr,char cmd) //Read Block Data transaction.
write_block_data(int addr,char cmd,long vals[]) //Write up to 32 bytes to a device.  This fucntion adds an initial byte indicating the length of the vals array before the valls array.  Use write_i2c_block_data instead!
long[] block_process_call(int addr,char cmd,long vals[]) //Block Process Call transaction.
I2C Access Functions
long[] read_i2c_block_data(int addr,char cmd) //Block Read transaction.
write_i2c_block_data(int addr,char cmd,long vals[]) //Block Write transaction.

'''




#DEVICE_REG_MODE1 = 0x00
#DEVICE_REG_LEDOUT0 = 0x1d

#Write a single register
#bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, 0x80)

#Write an array of registers
#ledout_values = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
#bus.write_i2c_block_data(DEVICE_ADDRESS, DEVICE_REG_LEDOUT0, ledout_values)



