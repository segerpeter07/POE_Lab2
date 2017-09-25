from serial import Serial, SerialException
import time
import string
import math
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import numpy.random
import termios

ser = Serial('/dev/ttyACM1', baudrate=9600)
# distances = [8,13,18,23,28,33,38,43,48,53,58]
distances = [58,53,48,43,38,33,28,23,18,13,8]
r = 0.04327906      # arm radius (m)


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
    plt.title('Figure Plot')
    plt.xlabel('xlabel')
    plt.ylabel('ylabel')
    plt.imshow(heatmap, extent=extent)
    plt.show()

def process_data(z):
    '''
    This function reads in the data from the serial bus and formats it correctly
    '''
    t0 = time.time()
    # tilt_angle = []
    # turn_angle = []
    # sensor_data = []
    data = []
    while((time.time() - t0) < 20):
        if ser.inWaiting >= 1:
            line = ser.readline()
            data.append(line)
            print line
            # data = line.split(' - ')
            # tilt_angle.append(data[0])
            # turn_angle.append(data[1])
            # end = data[2].split('\r')
            # val = end[0]
            # print val
            # # end = end[0]
            # sensor_data.append(calc_true_dist(int(val),z))
        time.sleep(0.4)
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
            if ser.in_waiting > 0:
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

def plot_calibration():
    x = distances
    y = []
    file = open('data', 'r')
    for line in file:
        if(type(int(line)) == int):
            y.append(line)
    area = 20
    colors = (0,0,0)
    plt.scatter(x, y, s=area, c=colors)
    plt.title('Calibration Data')
    plt.show()

def plot_calibration_linear(z):
    x = range(0,100)
    y = []
    for item in x:
        y.append(calc_true_dist(item, z))
    area = 6
    colors = (0,0,0)
    plt.scatter(x, y, s=area, c=colors)
    plt.title('Calibration Linear Fit')
    plt.show()


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
    z = np.polyfit(points, distances, 2)
    return z

def calc_true_dist(voltage, z):
    '''
    This function uses the calibration data to calculate the true distance
    read by the sensor
    '''
    dist = -int((z[0]*float(int(voltage)^2) + z[1]*float(int(voltage)) + z[2]))
    # dist = z[0]/(voltage-z[1])
    return dist

def calc_servo_x(tilt_angle):
    '''
    This function returns the calculated x distance from the servo
    '''
    return int(np.cos((180/np.pi)*tilt_angle-(180/np.pi)*135)*r)

def calc_servo_z(tilt_angle):
    '''
    This function returns the calculated z distance from the servo
    '''
    return int(np.sin((180/np.pi)*tilt_angle-(180/np.pi)*135)*r)

def calc_distances(tilt_angle, turn_angle, sensor_data):
    '''
    This function returns a tuple with the x, y, and z positions from the data
    '''
    for item in range(0,len(tilt_angle)-1):
        tilt_angle[item] = int(item)

    for item in range(0,len(turn_angle)-1):
        turn_angle[item] = int(item)

    for item in range(0, len(sensor_data)-1):
        sensor_data[item] = int(item)

    servo_x = calc_servo_x(tilt_angle)
    i = (servo_x + sensor_data)*np.cos(np.pi-(180/np.pi)*turn_angle)
    j = (servo_x + sensor_data)*np.sin((180/np.pi)*tilt_angle-(180/np.pi)*135)
    k = (servo_x + sensor_data)*np.cos((180/np.pi)*tilt_angle-(180/np.pi)*135)
    return i, j, k

def run_program(z):
    tilt_angle, turn_angle, sensor_data = process_data(z)
    #tilt_angle = int(tilt_angle)
    #turn_angle = int(turn_angle)
    #sensor_data = int(sensor_data)
    x, y, z = calc_distances(tilt_angle, turn_angle, sensor_data)
    gen_plot(x, y, z)

if __name__ == "__main__":
    # Collect Data
    # clear_data()
    # count = 0
    # gather_data(count)

    # path = '/dev/ttyACM1'

    # Disable reset after hangup
    # with open(path) as f:
    #     attrs = termios.tcgetattr(f)
    #     attrs[2] = attrs[2] & ~termios.HUPCL
    #     termios.tcsetattr(f, termios.TCSAFLUSH, attrs)
    #
    # ser = Serial(path, 9600)

    '''
    while(True):
        try:
            cmd_id = int(raw_input("Please enter a command ID (1 - read potentiometer, 2 - read the button: "))
        if int(cmd_id) > 2 or int(cmd_id) < 1:
            print "Values other than 1 or 2 are ignored."
        else:
            ser.write([int(cmd_id)])
            while ser.inWaiting() < 1:
                pass
            result = ser.readline()
            print result
    except ValueError:
        print "You must enter an integer value between 1 and 2."
    '''


    z = find_calibration()
    i = input('Press 1 to start...')
    if(i == 1):
        print "Starting"
        ser.write(int(i))
        run_program(z)
        ser.write(int(0))



    # Print equations
    # z = find_calibration()
    # print z
    # plot_calibration()
    # print 'y = ' + str(z[0]) + 'x + ' + str(z[1])
    # v = input("What is the voltage: ")
    # print calc_true_dist(v,z)

    # plot_calibration_linear(z)

    # Generate random data and plot it
    # tilt_angle, turn_angle, sensor_data = process_data(z)
    # x, y, z = calc_distances(tilt_angle, turn_angle, sensor_data)
    # gen_plot(x, y, z)
