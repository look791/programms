import serial
import time
import os
import ftplib
import sys

from datetime import datetime

print("****** Debugger v1.0 ******")
print("Podłącz konwerter USB-UART do pinów OUT8 i GND a z drugiej strony do raspberry, uruchom w ukrytej stronie mastera ext uart i upewnij się w trybie autorunning miga dioda RxD w konwerterze.")

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

filesize_MB = int(input('Wprowadź maksymalny rozmiar pliku [MB] (1MB to ok. 1 minuta pracy urządzenia): '))
filesize_b = filesize_MB*1024*1024
filename = time.strftime("log_%Y%m%d_%H%M%S")
filename_h = time.strftime("hex_%Y%m%d_%H%M%S")

size = 0
size_h = 0

while True:
        if (size_h < filesize_b):
                        #postać tekstowa utf-8
                        debug = open('{}.txt'.format(filename),"a", encoding='utf-8', errors='ignore')
                        path = '/home/pi/Python_scripts/''{}.txt'.format(filename)
                        path_ftp = '{}.txt'.format(filename)
                        ser_bytes = ser.readline()
                        ser_utf = ser_bytes.decode(encoding='utf-8', errors="ignore")
                        debug.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
                        debug.write(' ')
                        debug.write(ser_utf)
                        if sys.getsizeof(ser_bytes) == 33:
                            debug.write('\n')
                        print(time.strftime("%Y-%m-%d %H:%M:%S"))
                        print(ser_utf)

                        # postać hex
                        debug_h = open('{}.txt'.format(filename_h),"a",encoding='utf-8',errors='ignore')
                        path_h = '/home/pi/Python_scripts/''{}.txt'.format(filename_h)
                        path_h_ftp = '{}.txt'.format(filename_h)
                        x = ser_utf.encode('utf-8').hex()
                        debug_h.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
                        debug_h.write(' ')
                        debug_h.write(x)
                        debug_h.write('\n')
                        debug.close()
                        debug_h.close()
                        size = os.path.getsize(path)
                        size_h = os.path.getsize(path_h)
        else:
                        size = 0
                        size_h = 0
                        filename = time.strftime("log_%Y%m%d_%H%M%S")
                        filename_h = time.strftime("hex_%Y%m%d_%H%M%S")
