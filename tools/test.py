# Code example for get data from balance

import serial
import serial.tools.list_ports as port_list

def get_weight():
    ports = list(port_list.comports())
    for p in ports:
        print (p)

    if(ports):
        while True:
            com_serial = serial.Serial('/dev/ttyACM0', baudrate=9600, bytesize=8, parity='N', stopbits=1)
            com_serial.reset_input_buffer()
            data = com_serial.readline()
            print(data)
        # return data

get_weight()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

""" 
import subprocess
import time
import serial
import serial.tools.list_ports as port_list
ports = list(port_list.comports())
for p in ports:
    print (p)
# p = subprocess.Popen([r"C:\to\gsprint.exe", "test.pdf"], 
p = subprocess.Popen([r"C:\gs\gs9.52\bin\gswin64.exe", "C:\\Users\\ninaka\\use\\lambu\\dev\\client\\balance-project\\tools\\test.pdf"], 
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate()
print (stdout)
print (stderr) 
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
""" import time
import serial
import serial.tools.list_ports as port_list
ports = list(port_list.comports())
for p in ports:
    print (p)


com_serial = serial.Serial('COM3', baudrate=9600, bytesize=8, parity='N', stopbits=1)
com_serial.reset_input_buffer()


while True:
    respuesta = com_serial.readline()
    print(respuesta)
    # time.sleep(1)

print("out")
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

""" 
import serial
import time

z1baudrate = 115200
z1port = 'COM3'  # set the correct port before run it

z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2  # set read timeout
# print z1serial  # debug serial.
print ("is open? "+ str(z1serial.is_open))  # True for opened
if z1serial.is_open:
    while True:
        size = z1serial.inWaiting()
        print ("size? "+ str(size))  # True for opened
        if size:
            data = z1serial.read(size)
            print (data)
        else:
            print ('no data')
        time.sleep(1)
else:
    print ('z1serial not open')
"""