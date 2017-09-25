from serial import Serial, SerialException


cxn = Serial('/dev/ttyACM1', baudrate=9600)
run = True

while(run):
    try:
        cmd_id = int(input("Press 1 to start"))
        if int(cmd_id) > 2 or int(cmd_id) < 1:
            print("Values other than 1 or 2 are ignored.")
        else:
            cxn.write([int(cmd_id)])
            while cxn.inWaiting() < 1:
                pass
            reading = True
            while(reading):
                data = cxn.readline().split()
                print(data)
                file = open('image', 'a')
                file.write(str(data)+"\n")

    except ValueError:
        print("You must enter an integer value between 1 and 2.")
