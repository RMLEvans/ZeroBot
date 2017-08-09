import time, sys
import gpiozero as g0
from threading import Thread
import hcsr04sensor.sensor as sensor
IN1_m1 = g0.OutputDevice(17)
IN2_m1 = g0.OutputDevice(18)
IN3_m1 = g0.OutputDevice(21)
IN4_m1 = g0.OutputDevice(22)
StepPins_m1 = [IN1_m1,IN2_m1,IN3_m1,IN4_m1] # Motor 1 GPIO pins
IN4_m2 = g0.OutputDevice(19)
IN3_m2 = g0.OutputDevice(13)
IN2_m2 = g0.OutputDevice(5)
IN1_m2 = g0.OutputDevice(6)
StepPins_m2 = [IN1_m2,IN2_m2,IN3_m2,IN4_m2] # Motor 2 GPIO pins
Seq = [[0,0,1,1],  # Define step sequence.
       [0,0,1,0],  # Stepper motor contains four magnetic coils, 90 degrees apart.
       [0,1,1,0],  # Either a single coil or two adjacent coils can be activated, 
       [0,1,0,0],  # so 8 positions are possible, 45 degrees apart.
       [1,1,0,0],  # Activating them in sequence causes rotation.
       [1,0,0,0],  # Note there is gearing inside each motor unit (ratio 512:1 ?).
       [1,0,0,1],
       [0,0,0,1]]
StepCount = len(Seq)
all_clear = True
running = True

def bump_watch(): # thread to watch for obstacles
    global all_clear
    while running:
        value = sensor.Measurement(20, 16, 20, 'metric', 1)   # (trig_pin, echo_pin, temperature, unit, round_to)
        if value.raw_distance() < 10: # trigger if obstacle within 10cm
            all_clear = False
        else:
            all_clear = True

def move_bump(direction='F', motorSpeed=1, numsteps=2052):
    WaitTime = 10/float(10000) # adjust this to change speed
	if direction == 'L' or direction == 'F':
		leftStepSize = motorSpeed # Set to 1, 2 or 3 for forwards rotation. 3 is fastest (skipping motor positions, but lowest power.
	else:
		leftStepSize = -motorSpeed
	if direction == 'R' or direction == 'F':
		rightStepSize = motorSpeed
	else:
		rightStepSize = -motorSpeed
    leftStepCounter = 0
    rightStepCounter = 0
    counter = 0 # 4104 steps = 1 revolution
    while all_clear and counter < numsteps: # only move if no obstacles
		leftStepCounter = (leftStepCounter+leftStepSize+StepCount)%StepCount
		rightStepCounter = (rightStepCounter+rightStepSize+StepCount)%StepCount
		for pin in range(0, 4):
			Lpin = StepPins_m1[pin]
			Rpin = StepPins_m2[pin]
			if Seq[leftStepCounter][pin]==1:
				Lpin.on()
			else:
				Lpin.off()
			if Seq[rightStepCounter][pin]==1:
				Rpin.on() # Right wheel only
			else:
				Rpin.off()
		time.sleep(WaitTime)  #pause
		counter += motorSpeed

t1 = Thread(target=bump_watch) # run as seperate thread
t1.start() # start bump watch thread
for i in range(4): # Draw a right-handed square
    move_bump('F',3,4104)
    move_bump('R',3,2052)
running = False
