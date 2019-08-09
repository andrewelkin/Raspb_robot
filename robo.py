# by Carl Monk (@ForToffee)
# github.com/ForToffee/Robosapien
# based on work from http://playground.arduino.cc/Main/RoboSapienIR
# command codes originally from http://www.aibohack.com/robosap/ir_codes.htm

import time
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html


CYCLE = 833

##robo_prefix = 0x6   # 0110


class Robo(object):

	def __init__(self, pi,pin,prefix):

		self.pin = pin
		self.prefix = prefix
		self.pi = pi if pi is not None else pigpio.pi()
		self.pi.set_mode(pin, pigpio.OUTPUT) # IR TX connected to this GPIO.
		self.pi.write(self.pin, 1)
		self.pi.wave_clear()
		
		self.wf_head = self.add_wave(8, 8)
		self.wf_hi = self.add_wave(4, 1)
		self.wf_lo = self.add_wave(1, 1)
		self.wf_tail = self.add_wave(8, 8)
		
#		self.keep_alive = self.create_code(self.RSNoOp)
		


	def add_wave(self, hi, lo):
		self.pi.wave_add_generic([pigpio.pulse(1<<self.pin, 0, hi * CYCLE), pigpio.pulse(0, 1<<self.pin, lo * CYCLE)])
		return self.pi.wave_create()
	
	def create_code(self, code):
		data = code
		print data
		wave = []
		wave.append(self.wf_head)


		if self.prefix is not None:
			prefix = self.prefix
			for x in range(4):  # older 4 bits
				if (prefix & 8 != 0):
					wave.append(self.wf_hi)
#					print 1
				else:
					wave.append(self.wf_lo)
#					print 0
				prefix <<= 1

		for x in range(8):
			if (data & 128 != 0):
				wave.append(self.wf_hi)
#				print 1
			else:
				wave.append(self.wf_lo)
#				print 0
			data <<= 1

		wave.append(self.wf_tail)
		print wave
#		print "end"
		return wave

	def send_wave(self, wave):
		#print wave
		self.pi.wave_chain(wave)
		while self.pi.wave_tx_busy():
			time.sleep(0.002)

		self.pi.write(self.pin, 1)
	
	def send_code(self, code):
		self.send_wave(self.create_code(code))
		time.sleep(0.5)

	def clean_up(self):
		self.pi.wave_clear()

	


class RoboSapien(Robo):
	def __init__(self, pi,pin, prefix):

		self.RSTurnRight = 0x80
		self.RSRightArmUp = 0x81
		self.RSRightArmOut = 0x82
		self.RSTiltBodyRight = 0x83
		self.RSRightArmDown = 0x84
		self.RSRightArmIn = 0x85
		self.RSWalkForward = 0x86
		self.RSWalkBackward = 0x87
		self.RSTurnLeft = 0x88
		self.RSLeftArmUp = 0x89
		self.RSLeftArmOut = 0x8A
		self.RSTiltBodyLeft = 0x8B
		self.RSLeftArmDown = 0x8C
		self.RSLeftArmIn = 0x8D
		self.RSStop = 0x8E
		self.RSWakeUp = 0xB1
		self.RSBurp = 0xC2
		self.RSRightHandStrike = 0xC0
		self.RSNoOp = 0xEF


		Robo.__init__(self,pi,pin,None)



class RoboQuad(Robo):
	def __init__(self, pi,pin ):

		self.STOP = 0
		self.MOVE_FWD = 1
		self.MOVE_BACK = 2
		self.MOVE_LEFT = 3
		self.MOVE_RIGHT = 4

		self.TOPLEFT = 5
		self.TOPRIGHT= 6
		self.BOTTOMLEFT = 7
		self.BOTTOMRIGHT= 8

		self.SHIFT0 =0
		self.SHIFT1 =0x20
		self.SHIFT2 =0x40
		self.SHIFT3 =0x80

		self.ROTATE_CLK =9
		self.ROTATE_CNTRCLK =0xA

		self.WAKEUP = 0x81    # no-no shaking head if sleeping?

		self.SHAKE = 0x51
		self.NONO_QUICK_HEAD_SHAKE = 0x54


		self.SOUND_LOWER = 0x94  ## up to zero!


		self.LOOK_LEFT_UP_RIGHT_DOWN = 0xB4
		self.LOOK_RIGHT_UP_LEFT_DOWN = 0xB5


		self.LOOK_RIGHT_GO_RIGHT = 0xB6

		self.LOOK_ALL_AROUND = 0xB7


##
## B8 - BFnone

		Robo.__init__(self,pi,pin,0x6)










'''

Quad:
Commands (direction pad)
$600 + SHIFT ($600,$620,$640,$680) = stop
$601 + SHIFT ($601,$621,$641,$681) = forward
$602 + SHIFT ($602,$622,$642,$682) = backward
$603 + SHIFT ($603,$623,$643,$683) = left
$604 + SHIFT ($604,$624,$644,$684) = right
$605 + SHIFT ($605,$625,$645,$685) = top+left
$606 + SHIFT ($606,$626,$646,$686) = top+right
$607 + SHIFT ($607,$627,$647,$687) = bottom+left
$608 + SHIFT ($608,$628,$648,$688) = bottom+right 
SHIFT = $00 (shift level 1, LED off), $20 (shift level 2, green), $40 (shift level 3, orange) or $80 (shift level 4, red).
Special
$609 + SHIFT ($609,$629,$649,$689) = rotate clockwise
$60A + SHIFT ($60A,$62A,$64A,$68A) = rotate counter-clockwise
$610 + SHIFT ($610,$630,$650,$690) = autonomy button
$611 + SHIFT2 (n/a,$631,$651,$691) = activity shift combinations
$612 + SHIFT2 (n/a,$632,$652,$692) = aggression shift combinations
$613 + SHIFT2 (n/a,$633,$653,$693) = awareness shift combinations
$614 + SHIFT ($614,$634,$654,$694) = program button
$615 + SHIFT ($615,$635,$655,$695) = program play button
$616 + SHIFT ($616,$636,$656,$696) = demo 
SHIFT = $00 (shift level 1, LED off), $20 (shift level 2, green), $40 (shift level 3, orange) or $80 (shift level 4, red). 
SHIFT2 = $20 (shift level 2, green), $40 (shift level 3, orange) or $80 (shift level 4, red). When unshifted, toggles one attribute, then sends current personality state.
Personality setting (when any of 3 personality buttons pressed, no shift)
$6C0 + activity_level * 1 + awareness_level * 4 + aggression_level * $10 
activity/awareness/aggression level = 0 (low, green), 1 (medium, orange) or 2 (high, red)


UNKNOWN: $60B + SHIFT = ?
UNKNOWN: $60C + SHIFT = ?
UNKNOWN: $60D + SHIFT = ?
UNKNOWN: $60E + SHIFT = ?
UNKNOWN: $60F + SHIFT = ?
UNKNOWN: $617 and higher = ?
UNKNOWN: $611,$612,$613 = ? (not normally sent)
UNKNOWN: level = 3 ??? 

'''