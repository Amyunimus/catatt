
#!/usr/bin/env python
## Setup Section
from psychopy import core, visual, event
win = visual.Window([400,300], monitor="testMonitor")

# from rusocsci import buttonbox
# bb = buttonbox.Buttonbox()


response_clock = core.Clock()

response_clock.reset()
responded_time = response_clock.getTime()
print [('a',responded_time)]
core.wait(2)

response_clock.reset()
print event.getKeys(timeStamped=response_clock)



import serial
ser = serial.Serial()
ser.port = 'COM1'
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE

ser.open()

print ser.name
print ser

choices = ['a','b']
response_clock = core.Clock()



text_display = visual.TextStim(win, text="start experiment")
text_display.draw()
win.flip()
event.waitKeys(keyList=['x'])



text_display = visual.TextStim(win, text="Type a button")
text_display.draw()
win.flip()
core.wait(10)

choices = ['a','b']
##Get Keys
responded = ser.read()
responded_time = response_clock.getTime()
if responded in choices:
   print responded, responded_time
   #responded = [zip(responded,responded_time)]
else:
   responded = []

print responded


text_display = visual.TextStim(win, text="Type a button")
text_display.draw()
win.flip()

#Wait Keys
responded = False
while responded not in choices:
    responded = ser.read()
responded_time = response_clock.getTime()
#responded = [zip(responded,responded_time)]

print responded



core.wait(1)

for i in range(20): #use this for integers
   ser.write(chr(i))
   core.wait(.1)
   

core.wait(1)
for i in ['a','b','c','d']: #do not use chr for characters (but dont use characters either)
    ser.write(i)
    core.wait(.1)


ser.close()

## Cleanup Section
core.quit()