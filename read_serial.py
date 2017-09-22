from serial import Serial, SerialException
import time
import string
import matplotlib.pyplot as plt
import numpy as np

ser = Serial('/dev/ttyACM0', baudrate=9600)
distances = [8,13,18,23,28,33,38,43,48,53,58]

def clear_data():
    open('data', 'w').close()

def print_data():
    file = open('data', 'r')
    print file.read()
    file.close()

def read_data():
    file = open('data', 'a')
    while(True):
        file.write(ser.readline())

def plot_data():
    file = open('data', 'r')
    time = []
    data = []
    for line in file:
        split = line.split(' - ')
        split2 = split[1].split('\r')
        time.append(split[0])
        data.append(split2[0])
    for item in data:
        item = int(item)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(time, data)

    plt.savefig('example.png')

def gather_data(count):
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
    for num in distances:
        num = num*0.0254
    file = open('data', 'r')
    points = []
    for line in file:
        ins = line.split('\n')
        points.append(int(ins[0]))
    print points
    z = np.polyfit(points, distances, 1)
    return z

def calc_dist(voltage, z):
    dist = z[0]/(voltage-z[1])
    return dist


if __name__ == "__main__":
    # Collect Data
    # clear_data()
    # count = 0
    # gather_data(count)

    # print y
    # Print equations
    z = find_calibration()
    print 'y = ' + str(z[0]) + 'x + ' + str(z[1])
    v = input("What is the voltage: ")
    print calc_dist(v, z)
