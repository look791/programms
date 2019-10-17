import serial
import time
import os
import ftplib
import sys
import master01
from time import sleep
'''
#IP = input('Wprowadź adres IP czytnika: ')
IP = '172.16.0.192'
#PORT = input('Wprowadź port UDP: ')
PORT = 40192

Master = master01.Reader(IP, PORT)
fw_ver = Master.cmd(0x0F, context = None)
sleep(0.1)
hw_ver = Master.cmd(0x0E, context = None)
sleep(0.1)

print(fw_ver)
print(hw_ver[0])
'''
print("****** Debugger v1.0 ******")
print("Podłącz konwerter USB-UART do pinów OUT8 i GND a z drugiej strony do raspberry, uruchom w ukrytej stronie mastera ext uart i upewnij się w trybie autorunning miga dioda RxD w konwerterze.")

com = input('Wprowadź nr portu COM: ')
ser = serial.Serial(port='COM{}'.format(com), baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
#ser = serial.Serial(port='COM28', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

filesize_MB = int(input('Wprowadź maksymalny rozmiar pliku [MB] (1MB to ok. 1 minuta pracy urządzenia): '))
filesize_b = filesize_MB*1024*1024
filename = time.strftime("log_%Y%m%d_%H%M%S")
filename_h = time.strftime("hex_%Y%m%d_%H%M%S")

ftp = ftplib.FTP('172.16.0.111')
ftp.login('developer', 'smart123')
ftp.cwd('ftp/test')

size = 0
size_h = 0

while True:
        if (size_h < filesize_b):
                        #postać tekstowa utf-8
                        debug = open('{}.txt'.format(filename),"a",encoding='utf-8',errors='ignore')
                        path = 'C:/Users/Łukasz/Desktop/Python_scripts/''{}.txt'.format(filename)
                        path_ftp = '{}.txt'.format(filename)
                        ser_bytes = ser.readline()
                        ser_utf = ser_bytes.decode(encoding='utf-8', errors="ignore")
                        debug.write(time.strftime("%Y-%m-%d %H:%M:%S"))
                        debug.write(' ')
                        debug.write(ser_utf)
                        if sys.getsizeof(ser_bytes) == 33:
                            debug.write('\n')
                        print(time.strftime("%Y-%m-%d %H:%M:%S "))
                        print(ser_utf)

                        # postać hex
                        debug_h = open('{}.txt'.format(filename_h),"a",encoding='utf-8',errors='ignore')
                        path_h = 'C:/Users/Łukasz/Desktop/Python_scripts/''{}.txt'.format(filename_h)
                        path_h_ftp = '{}.txt'.format(filename_h)
                        x = ser_utf.encode('utf-8').hex()
                        debug_h.write(time.strftime("%Y-%m-%d %H:%M:%S"))
                        debug_h.write(' ')
                        debug_h.write(x)
                        debug_h.write('\n')
                        debug.close()
                        debug_h.close()
                        size = os.path.getsize(path)
                        size_h = os.path.getsize(path_h)
        else:
                        debug = open('{}.txt'.format(filename), "rb")
                        debug_h = open('{}.txt'.format(filename_h), "rb")
                        ftp.storlines('STOR ' + path_ftp, debug)
                        ftp.storlines('STOR ' + path_h_ftp, debug_h)
                        debug.close()
                        debug_h.close()
                        size = 0
                        size_h = 0
                        filename = time.strftime("log_%Y%m%d_%H%M%S")
                        filename_h = time.strftime("hex_%Y%m%d_%H%M%S")