import time
import os
import sys
from datetime import datetime
licznik = 1000
nr_user = 1
epc_nr = 10000000000000000000
while (licznik):
        #lista csv
        epc_pre = 'FFCC'
        lista = open('lista.csv',"a", encoding='utf-8', errors='ignore')
        lista.write('Imie{};'.format(nr_user))
        lista.write('Nazwisko{};'.format(nr_user))
        lista.write(epc_pre)
        lista.write(str(epc_nr))
        lista.write('\n')
        epc_nr = epc_nr + 1
        nr_user = nr_user + 1
        licznik = licznik - 1
