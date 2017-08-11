# ZeroBot

On-board code for robot based on the Raspberry Pi Zero.

See The MagPi Magazine Issue 40 - https://www.raspberrypi.org/magpi/issues/40/

------------------------------------------------------------------

Note that there is a mistake in the published article in MagPi 40.

The command to install the HCSR04 library should be:

    sudo pip3 install gpiozero hcsr04sensor

------------------------------------------------------------------



Program code in this repo has been updated for:

* Simultaneous independent control of left and right wheels (for quick turning on the spot).

* Included faster option, incrementing 3 steps at a time.

* Simplified program structure, with interpretation of direction code ('F', 'B', 'L' or 'R')
separated from central loop.

* More commenting, explaining stepper motor operation etc.

* A few more lines in main program, as example of responding to encountering an obstacle, instead of dropping out of program when all_clear==False.

* Motor step sequence re-ordered, so positive increments move forward.

* counter increments by motorStepSize, so it keeps track of distance travelled, irrespective of speed.

* Tidier code for looping the step counters, using modulo arithmetic (% notation).
