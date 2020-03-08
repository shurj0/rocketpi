import gpiozero
from time import sleep
from Rocket import Rocket
import csv

# Units are in metric, need to convert to imperial probably

mass = 43.06 # 95 lbs
cd = 0.005 
target_apogee = 3048 # 10,000 ft

# Create an instance of the rocket object, and set pins
# motor_right_pin = GPIO15
# motor_left_pin = GPIO21
# solenoid_pin = GPIO23

rocket = Rocket(mass, cd, 15, 21, 23)

# TODO: Define the sensor reader function here
# The function should return the values in the form of a tuple
# (altitude, velocity, acceleration)

def read_file(filename):
    with open(filename, 'r') as fp:
        reader = csv.reader(fp)
        # Creates a list of tuples, ignoring comments which begin with "#" in the csv file
        data = [ ( float(line[0]) , float(line[1]) * 0.3048, float(line[2]) * 0.3048, float(line[3]) *0.3048 ) for line in reader if line[0][0] != "#" ]
    return data

data = read_file("SimData.csv")

testVar = 0

def sensorReader():
    global testVar
    sensor_data = data[testVar]
    testVar += 1
    return sensor_data[1], sensor_data[2], sensor_data[3]

def launch(target_apogee):
    if rocket.fill_drain_open:
        rocket.close_fill_drain()
    # Countdown
    for i in range(10,0,-1):
        print(i)
        sleep(1)
    rocket.open_main()
    print("Control valve opened.")

    # Sets the altitude, velocity and acceleration in the rocket object and runs the predApogee() function. 
    # If the apogee returned by that function is greater than the target_apogee, the main valve is closed, and the loop is exited.
    # For optimal results, undervalue the target_apogee by around 500

    while rocket.main_valve_open:
        sensor_values = sensorReader()
        rocket.set_position(sensor_values[0])
        rocket.set_velocity(sensor_values[1])
        rocket.set_acceleration(sensor_values[2])
        predicted_apogee = rocket.predApogee(rocket.v)
        print(sensor_values, predicted_apogee)
        if predicted_apogee > target_apogee:
            rocket.close_main()
        # exits loop if the rocket never reaches the target_velocity
        if rocket.v < 0:
            break
        sleep(1)

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
    if command == "exit":
        break