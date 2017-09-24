from serial import Serial, SerialException
import time
import string
import math
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import numpy.random

ser = Serial('/dev/ttyACM0', baudrate=9600)
# distances = [8,13,18,23,28,33,38,43,48,53,58]
distances = [58,53,48,43,38,33,28,23,18,13,8]
r = 0.04327906      # arm radius (m)
z = ""

def clear_data():
    '''
    This function clears the data table
    '''
    open('data', 'w').close()

def print_data():
    '''
    This function prints everything in the table for debug purposes
    '''
    file = open('data', 'r')
    print file.read()
    file.close()

def read_data():
    file = open('data', 'a')
    while(True):
        file.write(ser.readline())

def gen_plot(x, y, z):
    '''
    This function generates a heatmap plot based off the given
    x and y values.
    '''
    # Create heatmap
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=(64,64), weights=z)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Plot graph
    plt.clf()
    plt.title('This is a title')
    plt.xlabel('xlabel')
    plt.ylabel('ylabel')
    plt.imshow(heatmap, extent=extent)
    plt.show()

def process_data():
    '''
    This function reads in the data from the serial bus and formats it correctly
    '''
    t0 = time.time()
    tilt_angle = []
    turn_angle = []
    sensor_data = []
    while((time.tim() - t0) < 30):
        if ser.in_waiting > 1:
            line = ser.readline()
            data = line.split(' - ')
            tilt_angle.append(data[0])
            turn_angle.append(data[1])
            sensor_data.append(calc_true_dist(data[2]))
    return tilt_angle, turn_angle, sensor_data

def gather_calibration_data(count):
    '''
    This function reads in data from serial bus and writes it to a file to be
    used to calibrate the sensor.
    '''
    while(count != 11):
        print "Sensing..."
        t0 = time.time()
        num_elements = 0
        dist = 0
        while((time.time() - t0) <= 5):
            if ser.in_waiting > 1:
                line = ser.readline().strip()
                try:
                    if(type(int(line)) == int):
                        dist += int(line)
                        num_elements += 1
                except ValueError:
                    print "Invalid value given"
                # if(type(int(line)) == 'int'):
                #     dist += int(line)
                #     num_elements += 1
        dist = dist/num_elements
        file = open('data', 'a')
        file.write(str(dist)+"\n")
        file.close()
        print "Move object..."
        time.sleep(3)
        count += 1

def find_calibration():
    '''
    This function performs a linear regression on the calibration data and sets
    z to be the equation of the data
    '''
    for num in distances:
        num = num*0.0254
    file = open('data', 'r')
    points = []
    for line in file:
        ins = line.split('\n')
        points.append(int(ins[0]))
    print points
    z = linregress(points, distances)
    return z

def calc_true_dist(voltage):
    '''
    This function uses the calibration data to calculate the true distance
    read by the sensor
    '''
    dist = z[0]/(voltage-z[1])
    return dist

def calc_servo_x(tilt_angle):
    '''
    This function returns the calculated x distance from the servo
    '''
    return np.cosd(tilt_angle-135)*r

def calc_servo_z(tilt_angle):
    '''
    This function returns the calculated z distance from the servo
    '''
    return np.sind(tilt_angle-135)*r

def calc_distances(tilt_angle, turn_angle, sensor_data):
    '''
    This function returns a tuple with the x, y, and z positions from the data
    '''
    servo_x = calc_servo_x(tilt_angle)
    i = (servo_x + sensor_data)*np.cosd(180-turn_angle)
    j = (servo_z + sensor_data)*np.sind(tilt_angle-135)
    k = (servo_x + sensor_data)*np.cosd(tilt_angle-135)
    return i, j, k

if __name__ == "__main__":
    # Collect Data
    # clear_data()
    # count = 0
    # gather_data(count)


    # Print equations
    # z = find_calibration()
    # print 'y = ' + str(z[0]) + 'x + ' + str(z[1])
    # v = input("What is the voltage: ")
    # print calc_true_dist(v)

    # Generate random data and plot it
    tilt_angle, turn_angle, sensor_data = process_data()
    x, y, z = calc_distances(tilt_angle, turn_angle, sensor_data)
    gen_plot(x, y, z)
