import gpiozero
from time import sleep
from Rocket import Rocket

# Units are in metric, need to convert to imperial probably

mass = 45 
cd = 0.05
target_apogee = 3300

# Create an instance of the rocket object, and set pins
# motor_right_pin = GPIO17
# motor_left_pin = GPIO18
# solenoid_pin = GPIO22

rocket = Rocket(mass, cd, 17, 18, 22)

# TODO: Define the sensor reader function here
# The function should return the values in the form of a tuple
# (altitude, velocity, acceleration)

def sensorReader():
    return (0,0,0)

def launch(target_apogee):
    if rocket.fill_drain_open:
        rocket.close_fill_drain()
    # Countdown
    for i in range(10,1,-1):
        print(i)
        sleep(1)
    rocket.open_main()
    print("Control valve opened.")

    # Sets the altitude, velocity and acceleration in the rocket object and runs the predApogee() function. 
    # If the apogee returned by that function is greater than the target_apogee, the main valve is closed, and the loop is exited.
    # For optimal results, undervalue the target_apogee by around 300, as the algorithm tends to overshoot a little by around that amount

    while rocket.main_valve_open:
        sensor_values = sensorReader()
        rocket.set_position(sensor_values[0])
        rocket.set_velocity(sensor_values[1])
        rocket.set_acceleration(sensor_values[2])
        predicted_apogee = rocket.predApogee(rocket.v)
        if predicted_apogee > target_apogee:
            rocket.close_main()

    return predicted_apogee

while True:
    command = input("Command: ")
    if command == "openmain":
        rocket.open_main()
    if command == "closemain":
        rocket.close_main()
    if command == "openfill":
        rocket.open_fill_drain()
    if command == "closefill":
        rocket.close_fill_drain()
    if command == "launch":
        print("Initiating launch sequence...")
        final_prediction = launch(target_apogee)
        print("Shutting down engine. Rocket should reach an apogee of {}.".format(final_prediction))
        break