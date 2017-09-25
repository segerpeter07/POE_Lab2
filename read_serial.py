from serial import Serial, SerialException
import time
import string
import math
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import numpy.random
import termios

# ser = Serial('/dev/ttyACM1', baudrate=9600)
# distances = [8,13,18,23,28,33,38,43,48,53,58]
distances = [58,53,48,43,38,33,28,23,18,13,8]

dist = []
for el in distances:
    dist.append(1.0/float(el))

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
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=(128,128), weights=z)
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
            #print line
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
    y = distances
    vol = []
    file = open('data', 'r')
    for line in file:
        if(type(int(line)) == int):
            vol.append(line)
    area = 20
    colors = (0,0,0)
    plt.clf()
    plt.scatter(dist, vol, s=area, c=colors)
    plt.title('Calibration Data')
    plt.show()

def plot_calibration_linear(z):
    y = range(0,100)
    x = []
    for item in y:
        x.append(calc_true_dist(item, z))
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
    # for num in distances:
    #     num = num*0.0254
    file = open('data', 'r')
    points = []
    for line in file:
        ins = line.split('\n')
        points.append(int(ins[0]))
    z = np.polyfit(dist, points, 2)
    return z

# def calc_true_dist(voltage, z):
#     '''
#     This function uses the calibration data to calculate the true distance
#     read by the sensor
#     '''
#     dist = -float((z[0]*float(int(voltage)^2) + z[1]*float(int(voltage)) + z[2]))
#     # dist = z[0]/(voltage-z[1])
#     return dist

def calc_true_dist(voltage, z):
    '''
    This function uses the calibration data to calculate the true distance
    read by the sensor
    '''
    dist = 0.01 * float((6787/(voltage-3))-4)
    # dist = z[0]/(voltage-z[1])
    return dist

def calc_servo_x(tilt_angle):
    '''
    This function returns the calculated x distance from the servo
    '''
    for i in tilt_angle:
        i = float(float(np.cos((np.pi/180)*i-(np.pi/180)*135))*r)
    return tilt_angle

def calc_servo_z(tilt_angle):
    '''
    This function returns the calculated z distance from the servo
    '''
    for i in tilt_angle:
        i = int(float(np.sin((np.pi/180)*i-(np.pi/180)*135))*r)
    return tilt_angle

def calc_distances(tilt_angle, turn_angle, sensor_data):
    '''
    This function returns a tuple with the x, y, and z positions from the data
    '''
    # for item in range(0,len(tilt_angle)-1):
    #     tilt_angle[item] = int(item)
    #
    # for item in range(0,len(turn_angle)-1):
    #     turn_angle[item] = int(item)
    #
    # for item in range(0, len(sensor_data)-1):
    #     sensor_data[item] = int(item)

    servo_x = calc_servo_x(tilt_angle)
    print type(sensor_data[6])
    print type(turn_angle[0])
    print type(tilt_angle[0])
    #cry = float(np.cos(np.pi-(180/np.pi)))
    #lul = float(np.cos(np.pi-(180/np.pi)))*turn_angle
    x_dist = []
    y_dist = []
    z_dist = []
    h = 0.05011     # height from sensor to base
    l = 0.22202     # dist from sensor to middle of plate
    # for i in range(0,len(servo_x)-1):
    #     i_dist.append(servo_x[i] + sensor_data[i] *float(np.cos(np.pi-(np.pi/180)))*turn_angle[i])
    #
    # for i in range(0,len(servo_x)-1):
    #     j_dist.append(servo_x[i] + sensor_data[i] *float(np.sin((np.pi/180))*tilt_angle[i]-(np.pi/180)*135))
    #
    # for i in range(0,len(servo_x)-1):
    #     k_dist.append(servo_x[i] + sensor_data[i] *float(np.cos((np.pi/180))*tilt_angle[i]-(np.pi/180)*135))

    for i in range(0,len(servo_x)-60):
        z_dist.append(h - (sensor_data[i])*(np.sin(tilt_angle[i]*(np.pi/180.0)-135.0*(np.pi/180.0))))

    for i in range(0,len(servo_x)-60):
        x_dist.append((l - ((sensor_data[i])*np.cos(tilt_angle[i]*(np.pi/180.0))-135.0*(np.pi/180.0)))*np.cos(turn_angle[i]*(np.pi/180.0)))

    for i in range(0,len(servo_x)-60):
        y_dist.append((l - ((sensor_data[i])*np.cos(tilt_angle[i]*(np.pi/180.0))-135.0*(np.pi/180.0)))*np.sin(turn_angle[i]*(np.pi/180.0)))


    return x_dist, y_dist, z_dist

def run_program(z):
    tilt_angle, turn_angle, sensor_data = process_data(z)
    #tilt_angle = int(tilt_angle)
    #turn_angle = int(turn_angle)
    #sensor_data = int(sensor_data)
    x, y, z = calc_distances(tilt_angle, turn_angle, sensor_data)
    gen_plot(x, y, z)

def parce_file(z):
    tilt_angle = []
    turn_angle = []
    sensor_data = []
    file = open('image', 'r')
    for line in file:
        parts = line.split("'")
        elements = parts[1].split(",")
        if(len(elements) == 3):
            tilt_angle.append(float(elements[0]))
            turn_angle.append(float(elements[1]))
            sensor_data.append(calc_true_dist(float(elements[2]), z))
    return tilt_angle, turn_angle, sensor_data

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


    z = find_calibration()
    # print z
    # i = input('Press 1 to start...')
    # if(i == 1):
    #     print "Starting"
    #     ser.write(int(i))
    #     run_program(z)
    #     ser.write(int(0))
    # print calc_true_dist('200',z)


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
    tilt_angle, turn_angle, sensor_data = parce_file(z)
    x, y, z = calc_distances(tilt_angle, turn_angle, sensor_data)
    print z
    gen_plot(x, y, z)
