import master01
import datetime as dt
from time import sleep

IP = '172.16.0.192'
PORT = 40192

frm_buz_on = [0xFF, 0x02, 0x00, 0x53, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0xFA, 0xFF]
frm_buz_off = [0xFF, 0x02, 0x00, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x56, 0xBF]
frm_ping = [0xFF, 0x00, 0x00, 0xF0, 0x00, 0x00, 0x00, 0x00, 0xC0, 0x88]

buz_on = bytearray(frm_buz_on)
buz_off = bytearray(frm_buz_off)
ping = bytearray(frm_ping)
i = 0
EPC = ['FFCC00000000000000000007', 'FFCC00000000000000000008', 'FFCC00000000000000000002', 'FFCC00000000000000000003', 'FFCC00000000000000000004', 'FFCC00000000000000000005']
Master = master01.Reader(IP, PORT)

while True:

        Tags = Master.read_tags()
        if len(Tags) > 0:
            log = open('log.txt', 'a')
            for tag in Tags:
                if tag.epc in EPC:
                    print(dt.datetime.now().strftime("%c"), f'ANT: {tag.ant}', f'EPC: {tag.epc}')
                    log.write(dt.datetime.now().strftime("%c"))
                    log.write(' ANT: ')
                    log.write(f'{tag.ant}')
                    log.write(' EPC: ')
                    log.write(tag.epc)
                    log.write('\r\n')
                    access_flag = True
                    while access_flag:
                            # włącz buzer cykliczne 100ms
                            Master.send(buz_on)
                            sleep(0.1)
                            data = Master.rec(3)
                            sleep(0.1)
                            # wyłącz buzzer
                            Master.send(buz_off)
                            sleep(0.05)
                            data1 = Master.rec(3)
                            access_flag = False
                else:
                    access_flag = False
                    i = i + 1
                    if i >= len(EPC):
                        i = 0;
                    else:
                        last = tag.epc[20:24]
                        print(f'Karta nieautoryzowana...{last}')
                        log.write(dt.datetime.now().strftime("%c"))
                        log.write(' ANT: ')
                        log.write(f'{tag.ant}')
                        log.write(' Karta nieautoryzowana: ')
                        log.write(last)
                        log.write('\r\n')
                        sleep(0.02)

pass
