import socket
import binascii
import crc as crc
from collections import namedtuple
from struct import unpack, unpack_from, calcsize, pack


class Opcode():
    # test commands
    TestCmd = 0x01
    # information commands
    GetGeneralSettings = 0x10
    GetNetworkSettings = 0x20
    GetRfidSettings = 0x30
    GetWiegandSettings = 0x40
    GetDiagStatus = 0x50
    GetGsmSettings = 0x80
    GetAutonomous = 0x90
    GetBluetoothSettings = 0xB0
    GetWlanSettings = 0xC0
    GetHardwareVer = 0x0E
    GetFirmwareVer = 0x0F
    # general settings
    SetDeviceMode = 0x11
    SetInterface = 0x12
    SetUseBuzzer = 0x13
    SetUseDhcp = 0x14
    SetUseGpioEvent = 0x15
    SetTriggerMode = 0x16
    SetAlivePacket = 0x17
    SetLatchMode = 0x18
    # network settings
    SetNetwork = 0x21
    SetServer = 0x22
    SetSntp = 0x23
    SetHttp = 0x24
    SetWebsocket = 0x25
    SetNetAndSrv = 0x26
    SetHostname = 0x27
    SetPassword = 0x28
    # rfid settings
    SetRfidAntennaPower = 0x31
    SetRfidScanTime = 0x32
    SetRfidAntennaPorts = 0x33
    SetRfidSingleAntenna = 0x34
    SetRfidGen2Protocol = 0x35
    SetRfidAutoPlus = 0x36
    SetRfidEnSmartMode = 0x37
    SetRfidUniqueByData = 0x38
    SetRfidAntsPower = 0x3A
    SetRfidFrqChans = 0x3C
    SetRfidEnableSelect = 0x3D
    SetRfidSelectMask = 0x3E
    SetRfidDefaults = 0x3F
    # wiegand settings
    SetWiegandPulseWidth = 0x41
    SetWiegandPulseInt = 0x42
    SetWiegandDataInt = 0x43
    SetWiegandDataIntMul = 0x44
    SetWiegandMode = 0x45
    SetWiegandBackoffTime = 0x46
    SetWiegandFlags = 0x47
    SetWiegandChannels = 0x48
    SetWiegandOption = 0x49
    # diagnostics
    SetRelay = 0x51
    SetGpio = 0x52
    SetBuzzer = 0x53
    # operating
    ReadTagMultiple = 0x61
    ReadDataFromTag = 0x62
    ReadDataFromSelTag = 0x63
    ReadTagWithData = 0x64
    LockTag = 0x65
    LockSelectedTag = 0x66
    KillTag = 0x67
    KillSelectedTag = 0x68
    WriteEpc = 0x69
    WriteSelectedEpc = 0x6A
    WriteData = 0x6B
    WriteSelectedData = 0x6C
    OnOffState = 0x6D
    # gsm
    GsmGetUsers = 0x81
    GsmAddUser = 0x82
    GsmDelUser = 0x83
    GsmDelAllUsers = 0x84
    SetGsmPhone = 0x85
    SetGsmFtp = 0x86
    # autonomous
    AutoSetFlags = 0x91
    AutoSetPrefix = 0x92
    AutoSetAction = 0x94
    AutoSetBackoff = 0x95
    AutoGetIDMap = 0x96
    AutoSetID = 0x97
    AutoGetNewLogs = 0x9A
    AutoResetLogPointer = 0x9B
    # data
    Tags = 0xA0
    Data = 0xA1
    TagsAndData = 0xA2
    UniqueTags = 0xA3
    GsmData = 0xA8
    InputChange = 0xA9
    Alive = 0xAA
    BtData = 0xAB
    Result = 0xAF
    # bluetooth
    SetBeacon = 0xB2
    # wlan
    WlanSetNetwork = 0xC1
    WlanSetInterface = 0xC2
    WlanSetWlan = 0xC3
    # other
    GetDate = 0xD0
    SetDate = 0xD1
    # maintanace
    Ping = 0xF0
    EnterBootloader = 0xFB
    Reset = 0xFF
    # hidden
    Rainbow = 0xE4


OP = Opcode()


class Tag():
    '''
    Tag class. Stores tag's metadata and epc number.
    '''

    def __init__(self, ant, count, time, rssi, len, epc_crc, epc):
        self.ant = ant
        self.count = count
        self.time = time
        self.rssi = rssi
        self.len = len
        self.epc_crc = epc_crc
        self.epc = epc

    def __repr__(self):
        return str(self.ant) + ' ' + str(self.count) + ' ' + str(self.time) + ' ' + str(self.rssi) + ' ' + str(self.len) + ' ' + str(self.epc_crc)+ ' ' + self.epc

    def __str__(self):
        return str(self.ant) + ' ' + str(self.count) + ' ' + str(self.time) + ' ' + str(self.rssi) + ' ' + str(self.len) + ' ' + str(self.epc_crc) + ' ' + self.epc


class Reader():
    '''
    Master01 reader class. Init gets IP address and UDP port for communication.
    '''

    def __init__(self, ip, port):
        # store ip address and port number
        self.ip = ip
        self.port = port
        # open socket for UDP communication
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind local port
        self.sock.bind(('', port))

    def send(self, frame):
        '''
        Send frame to reader.
        '''
        # time.sleep(1)
        # RES_FLAG = 0
        self.sock.sendto(frame, (self.ip, self.port))

    def rec(self, timeout):
        '''
        Receive one frame from reader.
        '''
        data, addr = self.sock.recvfrom(256 + 12)
        return data

    def read_tags(self):
        '''
        Send request for tags and parse response.
        '''
        tag_list = []
        # prepare frame
        frm = [0xFF, 0x00, 0x00, 0x61, 0x00, 0x00, 0x00, 0x00]
        ba = bytearray(frm)
        c = crc.calc_crc(frm, len(frm))
        ba.append((c & 0xFF00) >> 8)
        ba.append(c & 0xFF)
        # send it to reader
        self.send(ba)
        # get ack
        data = self.rec(2)
        if data[3] != 0x61:
            return tag_list
        # get tags
        md_flg = 1
        while md_flg == 1:
            data = self.rec(2)
            if data[3] != 0xA0:
                break
            md_flg = data[4] & (1 << 0)
            cnt = 0
            idx = 9
            while cnt < data[1]:
                if 0x1F == data[idx]:
                    ant = data[idx + 1] & 0x0F
                    count = data[idx + 2]
                    time = ""
                    for i in range(4):
                        time = "%02X" % data[idx + 3 + i] + time
                    time = int(time, 16)
                    rssi = data[idx + 7]
                    if rssi > 0x7F:
                        rssi -= 0x100
                    length = data[idx + 9]
                    epc_crc = 0
                    for i in range(2):
                        epc_crc <<= 8
                        epc_crc |= data[idx + 10 + i]
                    epc = ""
                    for i in range(length):
                        epc += "%02X" % data[idx + 12 + i]
                    cnt += 12 + length
                    idx += 12 + length
                    tag = Tag(ant, count, time, rssi, length, epc_crc, epc)
                    tag_list.append(tag)
                    # print("Tag: ", end='')
                    # print("%d %d %s %d %d 0x%02X %s" % (ant, count, time, rssi, length, epc_crc, epc) )

        return tag_list

    def write_sel_tag(self, mem, pwd, sel_data_len, epc_len, sel_data_addr, sel_data, new_epc):
        # prepare frame
        frm = [0xFF, 11 + 24, 0x00, 0x6A, 0x00, 0x00, 0x00, 0x00]
        data = [0x01, 0x00, 0x00, 0x00, 0x00, 0x60, 0x0C, 0x00, 0x00, 0x00, 0x00]
        frm += data
        for i in range(0, 12):
            tmp = sel_data[i * 2:i * 2 + 2]
            val = int(tmp, 16)
            frm.append(val)
        for i in range(0, 12):
            tmp = new_epc[i * 2:i * 2 + 2]
            val = int(tmp, 16)
            frm.append(val)
        ba = bytearray(frm)
        c = crc.calc_crc(frm, len(frm))
        ba.append((c & 0xFF00) >> 8)
        ba.append(c & 0xFF)
        self.send(ba)
        resp = self.rec(10)
        resp = self.rec(10)

    def cmd(self, opc, context=None):
        # build header
        frm = [0xFF, 0x00, 0x00, opc, 0x00, 0x00, 0x00, 0x00]
        # calculate and add crc to the frame
        ba = bytearray(frm)
        # call opcode's callback for data field
        if TxOpcClb[opc] is not None:
            data = TxOpcClb[opc](context)
        else:
            data = b''
        ba.extend(data)
        ba[1] = len(data)
        c = crc.calc_crc(ba, len(ba))
        ba.append((c & 0xFF00) >> 8)
        ba.append(c & 0xFF)
        # send the frame
        self.send(ba)
        # if one of hidden commands - return
        if opc == OP.Rainbow:
            return []
        # get response
        resp = self.rec(2)
        # check SOF
        if resp[0] != 0xFF:
            return False
        # check CRC
        cc = crc.calc_crc(resp, len(resp) - 2)
        ccs = '%04X' % cc
        ccb = binascii.a2b_hex(ccs)
        if ccb != resp[-2:]:
            return False
        # check opcode
        if opc != resp[3]:
            return False
        # run Rx Opcode
        if len(resp) > 11 and RxOpcClb[resp[3]] is not None:
            return RxOpcClb[resp[3]](resp[9:-2])
        else:
            return []

    def close(self):
        '''
        Close connection with Master01 reader.
        '''
        self.sock.close()

    def __exit__(self, *err):
        '''
        Closing app.
        '''
        self.close()

    def __del__(self):
        '''
        Deleting object.
        '''
        self.close()


#####################################################################
#                         CMD CALLBACKS                             #
#####################################################################
# TX CALLBACKS
def TxClbSetRfidScanTime(ScanTime):
    pck = pack('<HH', ScanTime.Read, ScanTime.Write)
    return pck


def TxClbRainbow(Led):
    return pack('<bbb', 0x45, Led[0], Led[1])


def TxClbSetRelay(Relays):
    mask = 0
    if len(Relays) == 0:
        pck = pack('<b', 0)
        return pck
    for rel in Relays:
        rel -= 1
        mask |= (1 << rel)
    pck = pack('<b', mask)
    return pck


# def TxClbNoData(context):
# 	return []

# RX CALLBACKS
def RxClbGetHardware(data):
    return data


def RxClbGetFirmware(data):
    fwver = (data[0], data[1], data[2])
    return fwver


def RxClbRfidSettings(data):
    idx = 0
    # ant
    frmt = '<bbb'
    frmt_len = calcsize(frmt)
    RfidAnt = RfidAnt_t._make(unpack(frmt, data[idx:idx + frmt_len]))
    idx += frmt_len
    # pwr
    frmt = '<HH'
    frmt_len = calcsize(frmt)
    PWR = []
    for i in range(8):
        RfidPwr = RfidPwr_t._make(unpack(frmt, data[idx:idx + frmt_len]))
        PWR.append(RfidPwr)
        idx += frmt_len
    # scan time
    frmt = '<HH'
    frmt_len = calcsize(frmt)
    SCAN_TIME = RfidScanTime_t._make(unpack(frmt, data[idx:idx + frmt_len]))
    idx += frmt_len
    # config
    frmt = '<I'
    frmt_len = calcsize(frmt)
    CONFIG = RfidConfig_t._make(unpack(frmt, data[idx:idx + frmt_len]))
    idx += frmt_len
    # select
    frmt = '<bHbI12s'
    frmt_len = calcsize(frmt)
    SELECT = RfidSelect_t._make(unpack(frmt, data[idx:idx + frmt_len]))
    idx += frmt_len
    # autorunning+
    frmt = '<bIb'
    frmt_len = calcsize(frmt)
    AUTORUNNING_PLUS = RfidAutorunningPlus_t._make(unpack(frmt, data[idx:idx + frmt_len]))
    idx += frmt_len
    # collect all
    RFID = RFID_t(RfidAnt, PWR, SCAN_TIME, CONFIG, SELECT, AUTORUNNING_PLUS)
    return RFID


def RxClbPing(data):
    return []


TxOpcClb = {
    OP.GetHardwareVer : None,					# GetHardware
    OP.GetFirmwareVer 	: None,					# GetFirmware
    OP.GetRfidSettings	: None,					# GetRfidSettings
    OP.SetRfidScanTime	: TxClbSetRfidScanTime,	# SetRfidScanTime
    OP.SetRelay			: TxClbSetRelay,		# SetRelay
    OP.Ping 			: None,					# Ping
    OP.Rainbow			: TxClbRainbow			# Rainbow
}

RxOpcClb = {
    OP.GetHardwareVer	: RxClbGetHardware,		# GetHardware
    OP.GetFirmwareVer	: RxClbGetFirmware,		# GetFirmware
    OP.GetRfidSettings	: RxClbRfidSettings,	# GetRfidSettings
    OP.SetRfidScanTime	: None,					# SetRfidScanTime
    OP.SetRelay			: None, 				# SetRelay
    OP.Ping				: RxClbPing,			# Ping
    OP.Rainbow			: None,					# Rainbow
}

#####################################################################
#                         DATA STRUCTURES                           #
#####################################################################
# RFID SETTINGS
RfidAnt_t = namedtuple('RfidAnt_t', 'Available '
                                    'Enabled '
                                    'Single')
RfidPwr_t = namedtuple('RfidPwr_t', 'WrPwr '
                                    'RdPwr')
RfidScanTime_t = namedtuple('ScanTime_t', 'Read '
                                          'Write')
RfidConfig_t = namedtuple('RfidConfig_t', 'Config')
RfidSelect_t = namedtuple('RfidSelect_t', 'Memory '
                                          'Offset '
                                          'Length '
                                          'Password '
                                          'Mask')
RfidAutorunningPlus_t = namedtuple('RfidAutorunningPlus_t', 'RdMemBank '
                                                            'RdDataAddr '
                                                            'RdCount')
RFID_t = namedtuple('RFID_t', 'ANT '
                              'PWR '
                              'SCAN_TIME '
                              'CONFIG '
                              'SELECT '
                              'AUTORUNNING_PLUS')