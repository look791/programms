def reverse_bits16(val):
    return int('{:016b}'.format(val)[::-1], 2)


def calc_crc(dat, size):
    POLY = 0x8408
    crc = 0xFFFF
    B = 0

    if size == 0:
        return ~crc & 0x0000

    for l in range(size):
        B = dat[l] & 0xFF
        for i in range(8):
            if ((crc & 0x0001) ^ (B & 0x0001)):
                crc = (crc >> 1) ^ POLY
            else:
                crc >>= 1
            B >>= 1
    return reverse_bits16(crc)
