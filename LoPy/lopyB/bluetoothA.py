import pycom
from network import Bluetooth

global data


def startSending(dataString: str):
    global data
    pycom.rgbled(0x70000ff)
    data = dataString
    bluetooth = Bluetooth()
    bluetooth.set_advertisement(name='Loy', service_uuid=b'1234567890123456')
    bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
    bluetooth.advertise(True)
    srv1 = bluetooth.service(uuid=b'serviceA90123456', isprimary=True)
    srv2 = bluetooth.service(uuid=b'serviceB90123456', isprimary=True)
    srv3 = bluetooth.service(uuid=b'serviceC90123456', isprimary=True)
    srv4 = bluetooth.service(uuid=b'serviceD90123456', isprimary=True)

    chr1 = srv1.characteristic(uuid=b'temp567890123456', value=dataString.split(":")[2])
    chr2 = srv2.characteristic(uuid=b'light67890123456', value=dataString.split(":")[1])
    chr3 = srv3.characteristic(uuid=b'time567890123456', value=dataString.split(":")[3])
    chr4 = srv4.characteristic(uuid=b'id34567890123456', value=dataString.split(":")[0])

    print(dataString)
    char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)
    char2_cb = chr2.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)
    char3_cb = chr3.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)
    char4_cb = chr4.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)


def conn_cb(bt_o):
    events = bt_o.events()
    if events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")


def char1_cb_handler(chr):
    events = chr.events()
    print("return")
    # return data
