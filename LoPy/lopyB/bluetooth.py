import pycom
from network import Bluetooth

global data
global call
global bluetooth

read = 0
global clear


def startSending(dataList: list, callback, shouldClear):
    global data
    global call
    global bluetooth
    global clear
    clear = shouldClear
    call = callback
    pycom.rgbled(0x70000ff)

    data = dataList
    print(str(data))
    bluetooth = Bluetooth()
    bluetooth.set_advertisement(name='Loy', service_uuid=b'1234567890123456')
    bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
    bluetooth.advertise(True)
    srv1 = bluetooth.service(uuid=b'serviceA90123456', isprimary=True)
    srv2 = bluetooth.service(uuid=b'serviceB90123456', isprimary=True)
    srv3 = bluetooth.service(uuid=b'serviceC90123456', isprimary=True)
    srv4 = bluetooth.service(uuid=b'serviceD90123456', isprimary=True)

    chr1 = srv1.characteristic(uuid=b'temp567890123456', value="")
    chr2 = srv2.characteristic(uuid=b'light67890123456', value="")
    chr3 = srv3.characteristic(uuid=b'time567890123456', value="")
    chr4 = srv4.characteristic(uuid=b'id34567890123456', value="")

    chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)
    chr2.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char2_cb_handler)
    chr3.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char3_cb_handler)
    chr4.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char4_cb_handler)


def inputToCharacteristics(type: int):
    global read1
    global read2
    global read3
    global read4
    print("1 " + str(read1) + " 2 " + str(read2) + " 3 " + str(read3) + " 4 " + str(
        read4))  # for debugging how far the data transfer is
    if read1 > len(data[0]) and read2 > len(data[0]) and read3 > len(data[0]) and read4 > len(data[0]):
        return ""  # signal aggregator that all data is read

    if type == 0:
        read1 += 1
        if read1 > len(data[0]): return "i" # means no more data on characteristic
        ret = data[0][read1 - 1]
        print(ret)
        return ret
    elif type == 1:
        read2 += 1
        if read2 > len(data[0]): return "i"
        ret = data[1][read2 - 1]
        print(ret)
        return ret
    elif type == 2:
        read3 += 1
        if read3 > len(data[0]): return "i"
        ret = data[2][read3 - 1]
        print(ret)
        return ret
    else:
        read4 += 1
        if read4 - 1 == len(data[0]) and read3 > len(data[0]): return ""
        if read4 > len(data[0]): return "i"
        ret = data[3][0]
        print(ret)
        return ret


def conn_cb(bt_o):
    global data
    events = bt_o.events()
    if events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        if (read4 - 1) >= len(data[0]) and read3 > len(data[0]):
            call(clear)
        print("disconnected")


read1 = 0


def char1_cb_handler(chr):
    return inputToCharacteristics(0)


read2 = 0


def char2_cb_handler(chr):
    return inputToCharacteristics(1)


read3 = 0


def char3_cb_handler(chr):
    return inputToCharacteristics(2)


read4 = 0


def char4_cb_handler(chr):
    return inputToCharacteristics(3)
