import serial
import serial.tools.list_ports as port_list
import time
from setting import BALANCE_CONF

def get_weight():
   value = -1
   weight_kg = '0'
   try:
      port = BALANCE_CONF['PORT']
      ports = list(port_list.comports())
      if(ports):
         com_serial = serial.Serial(port, baudrate=9600, bytesize=serial.EIGHTBITS, parity='N', stopbits=1)
         com_serial.reset_input_buffer()
         while (value== -1):
            data = com_serial.readline() # peso
            print(data)
            data= data.decode("utf-8") 
            value= data.lower().find('kg') # linea de peso
         weight_kg= data[:value].strip()
         return weight_kg, True
      else:
         # current_app.logger.warning('balance: no ports')
         return 0, False

   except Exception as e:
      print(e)
      # current_app.logger.error('%s', e)
      return 0, False