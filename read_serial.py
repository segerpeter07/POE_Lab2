from serial import Serial, SerialException
import time
import string
import matplotlib.pyplot as plt

ser = Serial('/dev/ttyACM0', baudrate=9600)

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

def gather_data():
    while(True):
        print "Sensing..."
        t0 = time.time()
        num_elements = 0
        dist = 0
        while((time.time() - t0) <= 5000):
            if ser.in_waiting > 1:
                line = ser.readline()
                if(line == int):
                    print "hello"
                # if(line != ""):
                #     print ser.readline()
                # dist += int(ser.readline())
                # num_elements += 1
        dist = dist/num_elements
        file = open('data', 'a')
        file.write(dist)
        file.close()
        print "Move object..."
        sleep(3)

if __name__ == "__main__":
    # clear_data()
    read_data()
    # print_data()
    # plot_data()
    # gather_data()
