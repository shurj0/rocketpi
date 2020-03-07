import gpiozero
from math import log
from time import sleep

class Rocket:
    def __init__(self, mass, cd, motor_right_pin, motor_left_pin, solenoid_pin):
        self.mass = mass
        self.cd = cd
        self.motor_right = gpiozero.DigitalOutputDevice(motor_right_pin)
        self.motor_left = gpiozero.DigitalOutputDevice(motor_left_pin)
        self.solenoid = gpiozero.DigitalOutputDevice(solenoid_pin)
        self.main_valve_open = False
        self.fill_drain_open = False

    # Define the control valve opening/closing functions for easier use and state checking.
    # Assumes control valve is closed at startup, since the wires being used with the driver
    # can't be used to check position of the stepper motor. 

    def open_main(self):
        self.motor_right.on()
        sleep(0.5)
        self.motor_right.off()
        self.main_valve_open = True

    
    def close_main(self):
        self.motor_left.on()
        sleep(0.5)
        self.motor_left.off()
        self.main_valve_open = False

    # MUST check that control valve is closed before opening fill/drain valve

    def open_fill_drain(self):
        if self.main_valve_open:
            self.close_main()
        self.solenoid.on()
        self.fill_drain_open = True
    
    def close_fill_drain(self):
        self.solenoid.off()
        self.fill_drain_open = False

    # Setters are used instead of manually changing class attributes

    def set_position(self, x):
        self.x = x
    
    def set_velocity(self, v):
        self.v = v
    
    def set_acceleration(self, a):
        self.a = a
    
    # Apogee calculator

    def predApogee(self, current_velocity):
        # Rename variables for cleaner calculation
        m = self.mass
        C = self.cd
        g = 9.81

        intermediate = 1 + (C * (current_velocity ** 2)) / (m * g)
        max_height = (m / (2*C)) * log(intermediate)

        return self.x + max_height
    
