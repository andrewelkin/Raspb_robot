import pigpio
import time,threading


notes = {
    'B0': 31,
    'C1': 33, 'CS1': 35,
    'D1': 37, 'DS1': 39,
    'EB1': 39,
    'E1': 41,
    'F1': 44, 'FS1': 46,
    'G1': 49, 'GS1': 52,
    'A1': 55, 'AS1': 58,
    'BB1': 58,
    'B1': 62,
    'C2': 65, 'CS2': 69,
    'D2': 73, 'DS2': 78,
    'EB2': 78,
    'E2': 82,
    'F2': 87, 'FS2': 93,
    'G2': 98, 'GS2': 104,
    'A2': 110, 'AS2': 117,
    'BB2': 123,
    'B2': 123,
    'C3': 131, 'CS3': 139,
    'D3': 147, 'DS3': 156,
    'EB3': 156,
    'E3': 165,
    'F3': 175, 'FS3': 185,
    'G3': 196, 'GS3': 208,
    'A3': 220, 'AS3': 233,
    'BB3': 233,
    'B3': 247,
    'C4': 262, 'CS4': 277,
    'D4': 294, 'DS4': 311,
    'EB4': 311,
    'E4': 330,
    'F4': 349, 'FS4': 370,
    'G4': 392, 'GS4': 415,
    'A4': 440, 'AS4': 466,
    'BB4': 466,
    'B4': 494,
    'C5': 523, 'CS5': 554,
    'D5': 587, 'DS5': 622,
    'EB5': 622,
    'E5': 659,
    'F5': 698, 'FS5': 740,
    'G5': 784, 'GS5': 831,
    'A5': 880, 'AS5': 932,
    'BB5': 932,
    'B5': 988,
    'C6': 1047, 'CS6': 1109,
    'D6': 1175, 'DS6': 1245,
    'EB6': 1245,
    'E6': 1319,
    'F6': 1397, 'FS6': 1480,
    'G6': 1568, 'GS6': 1661,
    'A6': 1760, 'AS6': 1865,
    'BB6': 1865,
    'B6': 1976,
    'C7': 2093, 'CS7': 2217,
    'D7': 2349, 'DS7': 2489,
    'EB7': 2489,
    'E7': 2637,
    'F7': 2794, 'FS7': 2960,
    'G7': 3136, 'GS7': 3322,
    'A7': 3520, 'AS7': 3729,
    'BB7': 3729,
    'B7': 3951,
    'C8': 4186, 'CS8': 4435,
    'D8': 4699, 'DS8': 4978
}

un_tone = ([
    notes['C4'], notes['C5'], notes['A3'], notes['A4'],
    notes['AS3'], notes['AS4'], 0,
    0,
    notes['C4'], notes['C5'], notes['A3'], notes['A4'],
    notes['AS3'], notes['AS4'], 0,
    0
    ],
[
    12, 12, 12, 12,
    12, 12, 6,
    3,
    12, 12, 12, 12,
    12, 12, 6,
    3,

    ])

st_tone = ([
    notes['G4'], notes['G4'], notes['G4'],
    notes['EB4'], 0, notes['BB4'], notes['G4'],
    notes['EB4'], 0, notes['BB4'], notes['G4'], 0
    ],
[
    2, 2, 2,
    4, 8, 6, 2,
    4, 8, 6, 2, 8,

    2, 2, 2,
    4, 8, 6, 2,
    4, 8, 6, 2, 8

])

po_tone = ([
    notes['A4'], notes['G4'], notes['A4'], notes['E4'], notes['C4'], notes['E4'], notes['A3']
    ],
[
    8, 8, 8, 8, 8, 8, 4,
    8, 8, 8, 8, 8, 8, 4,

    8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 4,
    ])

po2_tone = ([
    notes['A4'], notes['B4'], notes['C5'], notes['B4'], notes['C5'], notes['A4'], notes['B4'], notes['A4'], notes['B4'],
    notes['G4'],
    notes['A4'], notes['G4'], notes['A4'], notes['F4']
    ],
[
    8, 8, 8, 8, 8, 8, 4,
    8, 8, 8, 8, 8, 8, 4,

    8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 4,

])

tw_tone = ([
    notes['C4'], notes['C4'], notes['G4'], notes['G4'], notes['A4'], notes['A4'], notes['G4'],

    ],
[
    4, 4, 4, 4, 4, 4, 2,



])

tw2_tone = ([

    notes['F4'], notes['F4'], notes['E4'], notes['E4'], notes['D4'], notes['D4'], notes['C4']
    ],
[
    4, 4, 4, 4, 4, 4, 2,



])

class buzzer_play(threading.Thread):

    def __init__(self,pi=None,pin=6):
        threading.Thread.__init__(self)
        self.pi = pi if pi is not None else pigpio.pi()
        self.pin = pin
        pi.set_mode(self.pin, pigpio.INPUT)
        pi.set_mode(self.pin, pigpio.OUTPUT)
        self.tones = [un_tone,st_tone,po_tone,po2_tone,tw_tone,tw2_tone]
        self.needToStop = False
        self.tone_toplay = -1
        self.needTobreak = False



    def buzz(self,frequency, length):  # create the function "buzz" and feed it the pitch and duration)

        if (frequency == 0):
            time.sleep(length)
            return
        period = 1.0 / frequency  # in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
        delayValue = period / 2  # calcuate the time for half of the wave
        numCycles = int(length * frequency)  # the number of waves to produce is the duration times the frequency

        for i in range(numCycles):  # start a loop from 0 to the variable "cycles" calculated above

            pi.write(self.pin,1)
            time.sleep(delayValue)  # wait with pin 27 high
            pi.write(self.pin,0)
            time.sleep(delayValue)  # wait with pin 27 low


    def run(self):
        while not self.needToStop :
            if self.tone_toplay>=0:
                no = self.tone_toplay
                self.tone_toplay = -1

                print "playing tone ", no
                self.play_tone(no)

            time.sleep(0.1)


    def stop(self):
        self.needTobreak = True
        self.stop_playing()
        self.needToStop = True

    def add_play_tone(self,no):
        if no >= len(self.tones): return
        print "adding tone ", no
        self.needTobreak = True
        self.tone_toplay = no


    def play_tone(self,no, pause=0.5, pace=0.500):
        try:
            if no >= len(self.tones): return
            self.play(self.tones[no],pause,pace)
        except:
            self.stop_playing()


    def stop_playing(self):
        pi.write(self.pin, 0)

    def play(self,mel, pause, pace=0.800):
        self.needTobreak = False
        melody, tempo = mel
        for i in range(0, len(melody)):  # Play song
            if self.needTobreak:
                print "breaking playing"
                self.stop_playing()
                break;

            noteDuration = pace / tempo[i]
            self.buzz(melody[i], noteDuration)  # Change the frequency along the song note
            pauseBetweenNotes = noteDuration * pause
            time.sleep(pauseBetweenNotes)


if __name__ == '__main__':  # Program start from here

    global pi
    pi = pigpio.pi()  # Connect to Pi.
    if not pi.connected:
        pi = pigpio.pi("192.168.3.74")  # Connect to Pi.

    pl = buzzer_play(pi,6)
    pl.start()

    try:
        while True:
            try:
                inp = raw_input()
                no = int(inp)
                if no<0: break
            except:
                continue
            pl.add_play_tone(no)


    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print "User break"

    pl.stop()
    pl.join()

    print "Exiting"